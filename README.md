# langchain-dapr-bindings

A sample integrating Dapr AI bindings with langchain.

## Background

Langchain already has integrations for many different language models, so why is this needed? Each of those integrations requires very specific choices being made at application implementation time--which models to support and how to configure them--as well as imposes a set of dependencies on the application for each supported model.

With Dapr, the application can use langchain but in a way that allows those decisions to be made at deployment time, through configuration, without any changes to application code and does not impose model-specific dependencies on the application (aside from the Dapr langchain binding and Dapr Client SDK itself).

## Prerequisites

- [Python](https://www.python.org/) 3.10 or later
- [Dapr](https://dapr.io/) 1.10 or later
- [Langchain](https://github.com/hwchase17/langchain) 0.0.137 or later
- [Dapr AI Bindings](https://github.com/philliphoff/dapr-ai-bindings)

## Using the bindings

> This bindings package has not yet been published.

1. Install the Dapr AI bindings

   ```bash
   pip3 install daprai
   ```

1. In your Python module, import the types as needed

   ```python
   from daprai.langchain import (
      # A chat-based LLM that uses Dapr AI bindings
      ChatDaprAI

      # A completion-based LLM that uses Dapr AI bindings
      DaprAI

      # A memory component that uses Dapr state stores
      DaprMemory
   )
   ```

## Examples

This repo contains several examples of integrating Dapr with langchain.

| Example | Description |
|---|---|
| [DaprAI LLM](examples/daprai/README.md) | An example of using the Dapr AI bindings as language models in langchain. |
| [DaprAI Chat LLM](examples/chatdaprai/README.md) | An example of using the Dapr AI bindings as chat language models in langchain. |
| [DaprAI Memory](examples/daprmemory/README.md) | An example of using Dapr state stores as chat history memory in langchain. |

## Developing

1. Install the project in an editable mode

   ```bash
   pip3 install -e .
   ```

1. Install required packages

   ```bash
   pip3 install -r requirements.txt
   ```

1. Run one of the [examples](#examples)
