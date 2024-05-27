<h1 align="center">LFG, a terminal assistant</h1>

<div align="center">
  LFG is a Python script that helps you with Linux and macOS terminal commands. Just ask it a question, and it will use AI to suggest a command and explain what it does. If you like the suggestion, the script can automatically run the command for you in your terminal.
</div>
<br />

![Demo](example.png)

## Why & What?

- Github Copilot CLI syntax feels clunky to me
- Faster than using Gemini, ChatGPT, or Google in a browser
- Simpler to find answers without checking man pages
- NEW: Switching to the free GPT-4o model
- NEW: Now you can run commands right from this command-line interface

However, never trust the output entirely.

## Installation

```bash
# install pipx
brew install pipx

# add pipx binaries to path
pipx ensurepath

# restart your terminal
# install LFG
pipx install lfg-llama
```

## Usage

This executable is using OpenAI, that means you need and [API token](https://platform.openai.com/api-keys).

[GPT-4o](https://platform.openai.com/docs/models/gpt-4o) is free to use.

Add the token to your .bashrc/.zshrc and reload your terminal.

```
export OPENAI_API_KEY={replace_me}
```

You can use either of these commands

```bash
$ lfg <query>
$ ask <query>
```

Now you can use the executable

```bash
$ ask kill port 3000

fuser -k 3000/tcp

Explanation:
The `fuser` command identifies processes using files or sockets. The `-k` option is used to kill th
ose processes. Here, `3000/tcp` specifies the TCP port number 3000. This command effectively kills
any process currently using port 3000.

> Execute the command? (N/y):
```

Change the LLM

```bash
$ ask get pods from all namespaces

kubectl get pods --all-namespaces


Explanation:
The `kubectl get pods --all-namespaces` command lists all the pods across all namespaces in a Kuber
netes cluster. The `--all-namespaces` flag is used to fetch the pods from every namespace instead of the default namespace.

> Execute the command? (N/y):
```

### Development

```bash
pip install --user pipenv
pipenv --python 3.11
pipenv install

pipenv run lfg kill port 3000
```

### TODO

- Fix the setup and pyproject file, including github workflow for releasing the package
