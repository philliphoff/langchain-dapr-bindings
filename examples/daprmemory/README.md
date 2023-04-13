# Dapr AI Chat LLM Example

An example of using [Dapr state stores](https://docs.dapr.io/developing-applications/building-blocks/state-management/state-management-overview/) as chat history memory in [langchain](https://github.com/hwchase17/langchain).

## Prerequisites

- [Python](https://www.python.org/) 3.10 or later
- [Dapr](https://dapr.io/) 1.10 or later
- [Langchain](https://github.com/hwchase17/langchain) 0.0.137 or later
- [Dapr AI Bindings](https://github.com/philliphoff/dapr-ai-bindings)

The Dapr AI bindings assume you have created an Azure Open AI instance in Azure and deployed a language model named `gpt-4`. To use another language model service, update the `./resources/ai.yaml` in the example folder.

## Running locally

1. Add Azure Open AI endpoint and key and Redis host and password to a `secrets.json` file in the root of the repo

   ```json
   {
      "azure-open-ai-endpoint": "<Azure Open AI endpoint>",
      "azure-open-ai-key": "<Azure Open AI key>",

      "store-host": "<Redis host>",
      "store-password": "<Redis password>"
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

1. Start the Python module multiple times, specifying a session ID and prompt for the AI assistant

   ```bash
   python3 main.py "<session ID>" "<prompt>"
   ```

   The session ID is arbitrary.  Each prompt and response will be accumulated in the Dapr state store using the session ID as a key, which enables the AI assistant to maintain history of the chat. Using a new session ID will start a new chat session as there will be no prior history.

   For example:
   
   ```text
   > python3 main.py "100" "My name is Phil"
   Hello Phil! It's great to meet you. How can I help you today? Do you have any specific topics you would like to talk about or questions you would like to ask?

   > python3 main.py "100" "Do you remember my name?"
   Yes, I do remember your name. You mentioned that your name is Phil. It's nice to continue our conversation, Phil. What would you like to discuss?

   > python3 main.py "101" "Do you remember my name?"
   As an AI language model, I don't have the ability to remember past interactions or recall specific details like names from a conversation. Each time you ask me something, it's like starting a new conversation. If you tell me your name now, I can use it during this conversation.
   ```

   Note the change to the session ID in the last command, which causes the AI assistant to no longer have any prior chat history.