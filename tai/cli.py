import os
import sys
import re
import signal
from types import FrameType
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.markdown import Markdown
from openai import OpenAI
from google import genai
from google.genai import types
import anthropic
try:
    from tai.config import load_config, create_config
except ModuleNotFoundError:
    from config import load_config, create_config


class Provider:
    """A wrapper for different AI providers."""

    def __init__(self, config):
        self.config = config
        self.client = self._get_client()

    def _get_client(self):
        provider = self.config.get("provider")
        api_key = self.config.get("api_key")

        if provider == "openai":
            return OpenAI(api_key=api_key)
        elif provider == "openrouter":
            return OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        elif provider == "google":
            return genai.Client(api_key=api_key)
        elif provider == "anthropic":
            return anthropic.Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def send_chat_query(self, query, system_prompt):
        provider = self.config.get("provider")
        model = self.config.get("model")

        try:
            if provider in ["openai", "openrouter"]:
                return self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    model=model,
                    stream=True,
                )
            elif provider == "google":
                return self.client.models.generate_content_stream(
                    model=model,
                    contents=[query],
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt.strip()
                    ),
                )
            elif provider == "anthropic":
                return self.client.messages.create(
                    model=model,
                    system=system_prompt,
                    messages=[{"role": "user", "content": query}],
                    stream=True,
                )
        except Exception as e:
            Console().print(
                Panel(
                    f"[bold red]Error sending chat query: {e}[/bold red]",
                    title="API Error",
                    border_style="red",
                )
            )
            sys.exit(1)


class CommandLineInterface:
    """A command-line interface for interacting with AI providers."""

    def __init__(self, config) -> None:
        """Initializes the CommandLineInterface."""
        self.console = Console()
        self.config = config
        self.provider = Provider(self.config)

    def handle_sigint(self, signum: int, frame: FrameType) -> None:
        """Signal handler for Ctrl+C (SIGINT)."""
        self.console.print("\n[bold red]Ctrl+C detected. Exiting gracefully...[/bold red]")
        sys.exit(0)

    def _generate_system_prompt(self) -> str:
        """Returns the system prompt for the LLM interaction."""
        return """
        You are a system administrator and elite hacker that knows all about the terminal in linux and mac.
        I provide you with a question about a command, and you give me back a response which shows the command,
        then a short explanation. If you get asked about the command tai, reply "tai query" with explanation 'This is me'.
        It is important you do not return commands you do not know. If that is the case, just respond 'I do not know'.

        Return your answer as a markdown code block with the command and explanation as this example:
        ```bash
        ls -al
        ```

        Explanation: list files and folders.
        """

    def _handle_stream(self, stream) -> str:
        """
        Processes the output stream from the LLM, printing each response chunk.
        """
        response = []
        provider = self.config.get("provider")

        with self.console.status("[bold green]Waiting for response...[/bold green]"):
            for chunk in stream:
                content = None
                if provider in ["openai", "openrouter"]:
                    content = chunk.choices[0].delta.content
                elif provider == "google":
                    content = chunk.text
                elif provider == "anthropic":
                    content = chunk.delta.text
                else:
                    raise ValueError(f"Unknown provider: {provider}")

                if content:
                    response.append(content)

        return "".join(response)

    def _extract_command(self, text: str) -> str:
        """
        Extracts the command from the response.
        """
        pattern = r"```bash\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _edit_command(self, command: str) -> str:
        """
        Allows the user to edit the command before execution.
        """
        self.console.print(Panel(command, title="Edit Command", border_style="yellow"))
        edited_command = Prompt.ask(
            "[bold yellow]Press Enter to execute, or type to edit[/bold yellow]",
            default=command,
            show_default=False,
        )
        return edited_command.strip()

    def _execute_command(self, command: str) -> None:
        """
        Executes the command in the terminal.
        """
        if Confirm.ask(f"Execute the command: [bold green]{command}[/bold green]?"):
            os.system(command)
        elif Confirm.ask("[bold yellow]Edit command?[/bold yellow]"):
            edited_command = self._edit_command(command)
            os.system(edited_command)
        else:
            self.console.print("[bold red]Exiting...[/bold red]")

    def run(self, query: str) -> None:
        """Initializes the application and processes the query."""
        signal.signal(signal.SIGINT, self.handle_sigint)

        system_prompt = self._generate_system_prompt()
        stream = self.provider.send_chat_query(query, system_prompt)
        response = self._handle_stream(stream)
        command = self._extract_command(response)

        if command:
            self.console.print(Panel(Syntax(command, "bash"), title="Command", border_style="green"))
            self._execute_command(command)
        else:
            self.console.print(Panel(Markdown(response), title="Response", border_style="blue"))


def main() -> None:
    """Initializes and runs the command-line interface."""
    config = load_config()

    if not config:
        create_config()
        sys.exit(0)

    if len(sys.argv) < 2:
        console = Console()
        console.print(
            Panel(
                "[bold yellow]Usage: tai <query>[/bold yellow]",
                title="Info",
                border_style="yellow",
            )
        )
        sys.exit(1)

    cli = CommandLineInterface(config)
    query = " ".join(sys.argv[1:])
    cli.run(query)


if __name__ == "__main__":
    main()
