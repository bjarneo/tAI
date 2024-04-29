# LFG

> LFG, It Really Whips the Llama's Ass 🦙🦙🦙🦙

![Logo](./logo.png)

LFG is a command-line tool that intelligently helps you find the right terminal commands for your tasks. It taps into the vast knowledge of the LLAMA3 language model (via Ollama) to understand your natural language descriptions and provide you with the most relevant commands and explanations.

## Installation

Currently, it uses ollama to run everything locally.

```bash
# install ollama
https://ollama.com/download/

# install the llama3 LLM
ollama pull llama3

# start ollama
ollama server

# install pipx
brew install pipx

# add pipx binaries to path
pipx ensurepath

# restart your terminal
# install LFG
pipx install lfg-llama
```

## Usage

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
