from pprint import pprint
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from .nodes import assistant
from .tools import multiply, add, divide


def create_graph():
    # Build graph
    builder = StateGraph(MessagesState)
    # Define memory saver
    memory = MemorySaver()
    # Add nodes
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode([multiply, add, divide]))
    # Add edges
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    return builder.compile(checkpointer=memory)


if __name__ == "__main__":
    # Create graph
    graph = create_graph()
    # Specify a thread
    config = {"configurable": {"thread_id": "1"}}
    # Test graph
    messages = [HumanMessage(content="Multiply 2 by 2, then add 1")]
    messages = graph.invoke({"messages": messages}, config=config)

    # Get both the AI messages with tool calls and the tool calls themselves
    ai_messages_with_tool_calls = []
    tool_calls = []

    for m in messages["messages"]:
        if (
            isinstance(m, AIMessage)
            and "tool_calls" in m.additional_kwargs
            and m.additional_kwargs["tool_calls"]
        ):
            # Add the message to our list of AI messages with tool calls
            ai_messages_with_tool_calls.append(m.additional_kwargs["tool_calls"])

            # Add the tool calls to our list
            tool_calls.append(m.additional_kwargs["tool_calls"])

    # pprint(ai_messages_with_tool_calls)
    pprint(tool_calls)
    # pprint(tool_calls)
