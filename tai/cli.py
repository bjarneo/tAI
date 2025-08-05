#!/usr/bin/python3

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
import openai
from openai import OpenAI
from openai.types.chat import ChatCompletion


class CommandLineInterface:
    """A command-line interface for interacting with the OpenAI API."""

    def __init__(self) -> None:
        """Initializes the CommandLineInterface."""
        self.console = Console()
        self.client = self._get_openai_client()

    def handle_sigint(self, signum: int, frame: FrameType) -> None:
        """Signal handler for Ctrl+C (SIGINT)."""
        self.console.print("\n[bold red]Ctrl+C detected. Exiting gracefully...[/bold red]")
        sys.exit(0)

    def _get_openai_client(self) -> OpenAI:
        """
        Retrieves the OpenAI API key and creates an OpenAI client instance.
        """
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            self.console.print(
                Panel(
                    "[bold red]OPENAI_API_KEY environment variable is not set[/bold red]",
                    title="Error",
                    border_style="red",
                )
            )
            sys.exit(1)
        return OpenAI(api_key=api_key)

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

    def _handle_stream(self, stream: ChatCompletion) -> str:
        """
        Processes the output stream from the LLM, printing each response chunk.
        """
        response = []
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response.append(chunk.choices[0].delta.content)
        return "".join(response)

    def _send_chat_query(self, query: str) -> ChatCompletion:
        """
        Sends a query to the OpenAI API and handles the response.
        """
        try:
            stream = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self._generate_system_prompt()},
                    {"role": "user", "content": query},
                ],
                model="gpt-4o",
                stream=True,
            )
            return stream
        except openai.APIConnectionError as e:
            self.console.print(f"[bold red]The server could not be reached: {e.__cause__}[/bold red]")
        except openai.RateLimitError as e:
            self.console.print(f"[bold red]A 429 status code was received; we should back off a bit: {e}[/bold red]")
        except openai.APIStatusError as e:
            self.console.print(f"[bold red]Another non-200-range status code was received: {e.status_code} {e}[/bold red]")
        sys.exit(1)

    def _extract_command(self, text: str) -> str:
        """
        Extracts the command from the response.
        """
        pattern = r"```bash\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else ""

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

    def run(self) -> None:
        """Initializes the OpenAI client and processes the query."""
        signal.signal(signal.SIGINT, self.handle_sigint)

        if len(sys.argv) < 2:
            self.console.print(
                Panel(
                    "[bold yellow]Usage: tai <query>[/bold yellow]",
                    title="Info",
                    border_style="yellow",
                )
            )
            sys.exit(1)

        query = " ".join(sys.argv[1:])

        with self.console.status("[bold green]Waiting for response...[/bold green]"):
            stream = self._send_chat_query(query)
            response = self._handle_stream(stream)

        command = self._extract_command(response)

        if command:
            self.console.print(Panel(Syntax(command, "bash"), title="Command", border_style="green"))
            self._execute_command(command)
        else:
            self.console.print(Panel(Markdown(response), title="Response", border_style="blue"))


def main() -> None:
    """Initializes and runs the command-line interface."""
    cli = CommandLineInterface()
    cli.run()


if __name__ == "__main__":
    main()