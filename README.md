# LFG

> LFG, It Really Whips the Llama's Ass 🦙🦙🦙🦙

![Demo](example.gif)

LFG is a command-line tool that intelligently helps you find the right terminal commands for your tasks. Such sales pitch. This interface is using GPT-4o as an engine.

## Why?

- Firstly, this was created to test Ollama -> Groq
- I do not like the Github Copilot command-line
- Quicker than using Gemini/ChatGPT/Google directly via the browser interface
- Easier to find what needed without opening man pages
- NEW: Changing to GPT-4o model which is free

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

```
$ lfg query
```

Now you can use the executable

```bash
lfg "kill port 3000"

# Kill process listening on port 3000
lsof -i :3000 | xargs kill

```

Change the LLM

```bash
$ lfg "list ec2 pipe json jq get name" -m llama370b

# List EC2 instances with name

aws ec2 describe-instances --query 'Reservations[].Instances[]|{Name:Tags[?Key==`Name`]|[0].Value,I
nstanceId}' --output text | jq '.[] | {"Name", .Name, "InstanceId", .InstanceId}'

This command uses the AWS CLI to describe EC2 instances, and then pipes the output to `jq` to format the output in a JSON-like format, showing the instance name and ID.
```

### Development

```bash
pip install --user pipenv
pipenv --python 3.11
pipenv install

pipenv run lfg "kill port 3000"
```

### TODO

- Fix the setup and pyproject file, including github workflow for releasing the package
