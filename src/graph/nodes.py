from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from .tools import add, multiply, divide

# List of tools available to the LLM
tools = [add, multiply, divide]

# Initialize the LLM
llm = init_chat_model(model="gpt-4o")

# Bind the tools to the LLM
llm = llm.bind_tools(tools)


# Function to call the LLM with the tools
def assistant(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


# Function to call the LLM with the tools
def assistant(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


if __name__ == "__main__":
    # Test the tool calling LLM
    print(assistant({"messages": [HumanMessage(content="What is 2 multiplied by 2?")]}))
