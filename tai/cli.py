#!/usr/bin/python3

import os
import sys
import re
import signal
from types import FrameType
import openai
from openai import OpenAI
from openai.types.chat import ChatCompletion


def handle_sigint(signum: int, frame: FrameType) -> None:
    """Signal handler for Ctrl+C (SIGINT)."""
    print("\nCtrl+C detected. Exiting gracefully...")
    sys.exit(0)


def get_openai_client() -> OpenAI:
    """Retrieves the OpenAI API key and creates a OpenAI client instance.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    return OpenAI()


def generate_system_prompt() -> str:
    """Returns the system prompt for the LLM interaction."""

    return """
You are a system administrator and elite hacker that knows all about the terminal in linux and mac. I provide you with a question about a command, and you give me back a response which shows the command, then a short explanation. The command should be wrapped as a code block. If you get asked about the command tai, reply "tai query" with explanation 'This is me'. It is important you do not return commands you do not know. If that is the case, just respond 'I do not know'. The layout of your response should be as follows: ```\n{command}\n``` \n\n Explanation:\n {explanation}.
"""


def handle_stream(stream: ChatCompletion) -> str:
    """Processes the output stream from the LLM, printing each response chunk.

    Args:
        stream (ChatCompletion): An iterator of chunks representing
        LLM responses.
    """
    response = []

    for chunk in stream:
        if chunk.choices[0].delta.content:
            response.append(chunk.choices[0].delta.content)

            print(chunk.choices[0].delta.content, end="", flush=True)

    return "".join(response)


def send_chat_query(query: str, client: OpenAI) -> ChatCompletion:
    """Sends a query to the OpenAI API and handles the response.

    Args:
        query (str): The user's query.
        client (OpenAI): The OpenAI client instance.
    """
    try:
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": generate_system_prompt()},
                {"role": "user", "content": query},
            ],
            model="gpt-4o",
            stream=True,
        )

        return stream

    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        print(e.response)
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)


def extract_command(text: str) -> str:
    """Extracts the command from the response.

    Args:
        text (str): The response from the LLM.

    Returns:
        str: The command extracted from the response.
    """
    pattern = r"```\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        command = match.group(1)

        return command


def execute_command(command: str) -> None:
    """Executes the command in the terminal.

    Args:
        command (str): The command to execute.
    """
    query = input("\n\n> Execute the command? (N/y): ")
    if query.lower() == "y" or query.lower() == "yes":
        os.system(command)
    else:
        print("\nExiting...")


def main():
    """Initializes the OpenAI client, and processes the query."""

    signal.signal(signal.SIGINT, handle_sigint)

    if len(sys.argv) < 2:
        print("Usage: tai <query>")

        sys.exit(1)

    query = " ".join(sys.argv[1:])

    try:
        client = get_openai_client()
        stream = send_chat_query(query, client)

        response = handle_stream(stream)

        command = extract_command(response)

        if command:
            execute_command(command)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    sys.exit(main())
