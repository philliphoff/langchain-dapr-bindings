# Dapr AI Chat LLM Example

An example of using the [Dapr AI bindings](https://github.com/philliphoff/dapr-ai-bindings) as chat language models in [langchain](https://github.com/hwchase17/langchain).

## Prerequisites

- [Python](https://www.python.org/) 3.10 or later
- [Dapr](https://dapr.io/) 1.10 or later
- [Langchain](https://github.com/hwchase17/langchain) 0.0.137 or later
- [Dapr AI Bindings](https://github.com/philliphoff/dapr-ai-bindings)

The Dapr AI bindings assume you have created an Azure Open AI instance in Azure and deployed a language model named `gpt-4`. To use another language model service, update the `./resources/ai.yaml` in the example folder.

## Running locally

1. Add Azure Open AI endpoint and key to a `secrets.json` file in the root of the repo

   ```json
   {
      "azure-open-ai-endpoint": "<Azure Open AI endpoint>",
      "azure-open-ai-key": "<Azure Open AI key>",
   }
   ```

1. Start the Dapr AI bindings pluggable component

   ```bash
   cd <dapr-ai-bindings source>/src/DaprAi.Components
   dotnet run
   ```

1. Start the Dapr sidecar

   ```bash
   dapr run --app-id daprai --dapr-grpc-port 50001 --resources-path ./resources
   ```
1. Start the Python module
   ```bash
   python3 main.py
   ```

1. Observe the output:

   ```text
   J'adore la programmation.
   ```

   > Due to variability in the language model response, you might get a different (but hopefully still correct) answer.
