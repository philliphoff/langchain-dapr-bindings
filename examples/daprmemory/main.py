import sys

from daprai.langchain import (
    ChatDaprAI,
    DaprMemory
)
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain

args = sys.argv[1:]

session_id = args[0]
input = args[1]

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = ChatDaprAI(componentName="ai")

memory = DaprMemory(
    componentName="store",
    return_messages=True,
    session_id=session_id)

# Initialize the memory with any existing history
memory.init()

conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

print(conversation.predict(input=input))
