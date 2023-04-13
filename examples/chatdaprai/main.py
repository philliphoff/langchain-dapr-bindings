from langchain.schema import HumanMessage
from daprai.langchain import ChatDaprAI

chat = ChatDaprAI(componentName="ai")

response = chat([HumanMessage(content="Translate this sentence from English to French. I love programming.")])

print(response.content)
