import json
from typing import Any, Dict, List, Optional

from dapr.clients import DaprClient
from langchain.memory.chat_memory import BaseChatMemory
from langchain.schema import get_buffer_string

from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatResult,
    HumanMessage,
    SystemMessage
)

def getChatHistoryMessageRole(message: BaseMessage) -> str:
    """Return the role for a given chat history message."""
    if isinstance(message, HumanMessage):
        return "Human"
    elif isinstance(message, AIMessage):
        return "AI"
    else:
        raise ValueError("Unknown message type.")

def createChatHistoryMessage(message: BaseMessage) -> Dict[str, str]:
    """Create a chat history message."""
    return {
        "role": getChatHistoryMessageRole(message),
        "content": message.content,
    }

class DaprMemory(BaseChatMemory):

    address: str | None = None
    componentName: str

    memory_key = "history"
    session_id: str

    def init(self) -> None:
        with DaprClient(address=self.address) as d:
            response = d.get_state(
                store_name=self.componentName,
                key=self.session_id)

        if (len(response.data) == 0):
            return

        responseJson = response.json()
        
        messages = responseJson.get("messages", [])

        for message in messages:
            if message["role"] == "AI":
                self.chat_memory.add_ai_message(message["content"])
            else:
                self.chat_memory.add_user_message(message["content"])

    def load_memory_variables(self, values: Dict[str, Any]) -> Dict[str, Any]:
        if self.return_messages:
            return {self.memory_key: self.chat_memory.messages}
        else:
            return {self.memory_key: get_buffer_string(self.chat_memory.messages)}

    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        input_str, output_str = self._get_input_output(inputs, outputs)
        messages = list(map(createChatHistoryMessage, self.chat_memory.messages))
        messages.append({"role": "Human", "content": f"{input_str}"})
        messages.append({"role": "AI", "content": f"{output_str}"})
        value = {
            "messages": messages
        }
        valueJson = json.dumps(value)
        with DaprClient(address=self.address) as d:
            self.chat_memory.messages
            d.save_state(
                store_name=self.componentName,
                key=self.session_id,
                value=valueJson)

        super().save_context(inputs, outputs)
