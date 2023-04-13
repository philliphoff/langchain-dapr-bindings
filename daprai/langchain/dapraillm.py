import json

"""Wrapper around Dapr AI bindings."""
from dapr.clients import DaprClient
from langchain.llms.base import LLM
from langchain.requests import TextRequestsWrapper
from typing import Any, List, Mapping, Optional

class DaprAI(LLM):
    """Wrapper around Dapr AI large language model bindings.

    To use, you should have the ``dapr`` python package installed.

    Example:
        .. code-block:: python

            from dapr import DaprAI
            openai = DaprAI(httpPort=3500, componentName="azure-open-ai-gpt-4")
    """

    address: str | None = None
    componentName: str

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "daprai"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the binding's completeText operation."""
        request = json.dumps({
            "user": prompt
        })
        with DaprClient(address=self.address) as d:
            response = d.invoke_binding(
                binding_name= self.componentName,
                operation="completeText",
                data=request)
            responseJson = response.json()
            return str(responseJson["assistant"])

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return { "componentName": self.componentName }
