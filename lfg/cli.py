#!/usr/bin/python3

import os
import sys
import openai
from openai import OpenAI
from openai.types.chat import ChatCompletion


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
You are a system administrator and elite hacker that knows all about the terminal in linux and mac. I provide you with a question about a command, and you give me back a response which shows the command, then a short explanation. The command should be wrapped as a code block. If you get asked about the command lfg, reply "lfg query" with explanation 'This is me'. It is important you do not return commands you do not know. If that is the case, just respond 'I do not know'. The layout of your response should be as follows: ```\n{command}\n``` \n\n Explanation:\n {explanation}.
"""


def handle_stream(stream: ChatCompletion) -> None:
    """Processes the output stream from the LLM, printing each response chunk.

    Args:
        stream (ChatCompletion): An iterator of chunks representing
        LLM responses.
    """
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)


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


def main():
    """Initializes the OpenAI client, and processes the query."""

    if len(sys.argv) < 2:
        print("Usage: ask <query>")

        sys.exit(1)

    query = " ".join(sys.argv[1:])

    try:
        client = get_openai_client()
        stream = send_chat_query(query, client)

        handle_stream(stream)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    sys.exit(main())
