#!/usr/bin/python3

import os
import sys
import argparse
import json
from groq import Groq


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def chat(ask):
    system_prompt = "From now on you should act as a system administrator / hacker that is really good at the terminal in linux and mac. All answers should be commands, and nothing else than commands and max 3 commands based on what the user asks for. All should be shown as a command using a bash markdown code block. Commands prefixed with. First the header before code block should be prefixed with # and added before the code block. Then the code block. Then add a short explanation after the code block."

    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ask},
        ],
        model="llama3-8b-8192",
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content != None:
            print(chunk.choices[0].delta.content, end="", flush=True)


def main(arg=None):
    parser = argparse.ArgumentParser(
        description="Use LFG to chat with the Llama as a sysadmin / haxor. \nExample: lfg 'how to kill a process in linux?'"
    )

    if arg:
        chat(" ".join(arg))


sys.exit(main(sys.argv[1:]))
