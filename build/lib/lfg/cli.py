#!/usr/bin/python3

import sys
import argparse
import json
import ollama


def chat(ask):
    data = "From now on you should act as a system administrator / hacker that is really good at the terminal in linux and mac. All answers should be commands, and nothing else than commands and max 3 commands based on what the user asks for. All should be shown as a command using a bash markdown code block. Commands prefixed with. First the header before code block should be prefixed with # and added before the code block. Then the code block. Then add a short explanation after the code block."

    stream = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": data},
            {"role": "user", "content": ask},
        ],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)


def main(arg=None):
    parser = argparse.ArgumentParser(
        description="Use LFG to chat with the Llama as a sysadmin / haxor. \nExample: lfg 'how to kill a process in linux?'"
    )

    if arg:
        chat(" ".join(arg))


sys.exit(main(sys.argv[1:]))
