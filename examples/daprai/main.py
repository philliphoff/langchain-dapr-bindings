from daprai.langchain import DaprAI

llm = DaprAI(componentName="ai")

text = "What would be a good company name for a company that makes colorful socks?"

print(llm(text))
