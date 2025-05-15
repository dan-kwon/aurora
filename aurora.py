import streamlit as st
from langchain_core.messages import HumanMessage
from src.graph.builder import create_graph

# Set the title of the app
st.title("Aurora")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(f"{message['content']}")


if prompt := st.chat_input(placeholder="How are you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        stream = st.session_state.graph.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={"configurable": {"thread_id": "1"}},
        )
        response = stream["messages"][-1].content
        st.markdown(response)
        st.session_state.tool_calls = stream["messages"]

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.markdown("## Tool Calls")
    st.markdown(st.session_state.tool_calls)
