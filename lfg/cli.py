#!/usr/bin/python3

import os
import sys
import json
from groq import Groq


def get_groq_client():
    """Retrieves the GROQ API key and creates a Groq client instance.

    Raises:
        ValueError: If the GROQ_API_KEY environment variable is not set.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    return Groq(api_key=api_key)


def generate_system_prompt():
    """Returns the system prompt for the LLM interaction."""
    return """
From now on you should act as a system administrator / hacker that is really good at the terminal in linux and mac. All answers should be commands, and nothing else than commands and max 3 commands based on what the user asks for. All should be shown as a command using a bash markdown code block. Commands prefixed with. First the header before code block should be prefixed with # and added before the code block. Then the code block. Then add a short explanation after the code block.
"""


def send_chat_query(query, client):
    """Sends a query to the Groq API and handles the response.

    Args:
        query (str): The user's query.
        client (Groq): The Groq client instance.
    """
    try:
        client = get_groq_client()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": generate_system_prompt()},
                {"role": "user", "content": query},
            ],
            model="llama3-8b-8192",
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
    except groq.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except groq.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit. Rate limited.")
    except groq.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)


def main():
    """Initializes the Groq client, and processes the query."""
    args = sys.argv[1:]
    if not args:
        parser.print_help()
        return

    try:
        client = get_groq_client()
        query = " ".join(args)

        send_chat_query(query, client)

        return
    except ValueError as e:
        print(f"Error: {e}")

        return


if __name__ == "__main__":
    sys.exit(main())
