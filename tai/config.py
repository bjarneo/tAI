import os
import json
import inquirer
from rich.console import Console
from rich.panel import Panel

CONFIG_DIR = os.path.expanduser("~/.config/tai")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
CONSOLE = Console()

MODELS = {
    "openai": ["gpt-4.1-mini", "o4-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    "google": ["gemini-2.5-flash", "gemini-2.5-pro"],
    "anthropic": ["claude-sonnet-4-20250514", "claude-3-5-haiku-20241022"],
    "openrouter": ["openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet", "google/gemini-2.5-flash"],
}

def load_config():
    """
    Loads the configuration from the config file.
    Returns the config dictionary or None if it doesn't exist or is invalid.
    """
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        CONSOLE.print(
            Panel(
                f"[bold red]Error reading config file at {CONFIG_PATH}: {e}. Please fix or delete it.[/bold red]",
                title="Configuration Error",
                border_style="red",
            )
        )
        return None

def create_config():
    """
    Prompts the user to create a new configuration file and saves it.
    """
    CONSOLE.print(
        Panel(
            "[bold yellow]Welcome to tAI! Let's set up your configuration.[/bold yellow]",
            title="tAI Setup",
            border_style="yellow",
        )
    )

    questions = [
        inquirer.List(
            "provider",
            message="Choose your AI provider",
            choices=list(MODELS.keys()),
        ),
    ]
    answers = inquirer.prompt(questions)
    provider = answers["provider"]

    model_choices = MODELS.get(provider, [])
    if model_choices:
        model_questions = [
            inquirer.List(
                "model_choice",
                message="Choose a model (or enter a custom model name)",
                choices=model_choices + ["custom"],
            ),
        ]
        answers.update(inquirer.prompt(model_questions))
        if answers["model_choice"] == "custom":
            custom_answer = inquirer.prompt(
                [inquirer.Text("model", message="Enter custom model name")]
            )
            answers["model"] = custom_answer["model"].strip()
        else:
            answers["model"] = answers["model_choice"]
    else:
        answers.update(
            inquirer.prompt([inquirer.Text("model", message="Enter model name")])
        )

    answers.update(
        inquirer.prompt(
            [inquirer.Password("api_key", message=f"Enter your {provider.capitalize()} API key")]
        )
    )

    config = {
        "provider": answers["provider"],
        "api_key": answers["api_key"],
        "model": answers["model"],
    }

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    CONSOLE.print(
        Panel(
            f"[bold green]Configuration saved successfully to {CONFIG_PATH}.\nYou can now run 'tai <your-query>'.[/bold green]",
            title="Setup Complete",
            border_style="green",
        )
    )
