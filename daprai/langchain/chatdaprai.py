import json

"""Wrapper around Dapr AI Chat bindings."""
from langchain.chat_models.base import (
    SimpleChatModel
)
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatResult,
    HumanMessage,
    SystemMessage
)
from dapr.clients import DaprClient
from typing import Dict, List, Optional

def getChatHistoryMessageRole(message: BaseMessage) -> str:
    """Return the role for a given chat history message."""
    if isinstance(message, HumanMessage):
        return "user"
    elif isinstance(message, AIMessage):
        return "assistant"
    elif isinstance(message, SystemMessage):
        return "system"
    else:
        raise ValueError("Unknown message type.")

def createChatHistoryMessage(message: BaseMessage) -> Dict[str, str]:
    """Create a chat history message."""
    return {
        "role": getChatHistoryMessageRole(message),
        "message": message.content,
    }

class ChatDaprAI(SimpleChatModel):
    """Wrapper around Dapr AI large language model bindings.

    To use, you should have the ``dapr`` python package installed.

    Example:
        .. code-block:: python

            from dapr import DaprAI
            openai = DaprAI(httpPort=3500, componentName="azure-open-ai-gpt-4")
    """

    address: str | None = None
    componentName: str

    def _call(
        self, messages: List[BaseMessage], stop: Optional[List[str]] = None
    ) -> str:
        """Call the binding's completeText operation."""
        humanMessage = messages[-1]
        if not isinstance(humanMessage, HumanMessage):
            raise ValueError("The last message must be a HumanMessage.")
        prompt = humanMessage.content
        request = {
            "history": {
                "items": list(map(createChatHistoryMessage, messages[:-1]))
            },
            "user": prompt
        }
        requestJson = json.dumps(request)
        with DaprClient(address=self.address) as d:
            response = d.invoke_binding(
                binding_name= self.componentName,
                operation="completeText",
                data=requestJson)
            responseJson = response.json()
            return str(responseJson["assistant"])

    async def _agenerate(
            self, messages: List[BaseMessage], stop: Optional[List[str]] = None
        ) -> ChatResult:
        raise NotImplementedError("Async generation not implemented for this LLM.")
