# LFG

> LFG, It Really Whips the Llama's Ass 🦙🦙🦙🦙

![Logo](./logo.png)

LFG is a command-line tool that intelligently helps you find the right terminal commands for your tasks. It taps into the vast knowledge of the LLAMA3 language model (via Ollama) to understand your natural language descriptions and provide you with the most relevant commands and explanations.

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

This executable is using Groq, that means you need and [API token](https://console.groq.com/keys).

Add the token to your .bashrc/.zshrc and reload your terminal.

```
export GROQ_API_KEY=1337
```

Now you can use the executable

```bash
lfg kill port 3000

# Kill process listening on port 3000
lsof -i :3000 | xargs kill

```

### Development

```bash
pip install --user pipenv
pipenv --python 3.7
pipenv install
```

### TODO

- Use the model directly without ollama
