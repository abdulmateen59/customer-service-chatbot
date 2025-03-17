import streamlit as st
import uuid
from langchain_core.messages import HumanMessage, ToolMessage
from agent import agent_workflow  # Ensure correct import

# Set Streamlit page config
st.set_page_config(
    page_title="e-com chatbot",
    page_icon="🛍️",
)

# Generate a unique thread ID for session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Streamlit App UI
st.title("🧸 Chatbot")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, content in st.session_state.chat_history:
    avatar = "🧸" if role == "assistant" else "👤"
    with st.chat_message(avatar):
        st.write(content)

# User input
config = {"configurable": {"thread_id": st.session_state.thread_id}}

user_input = st.chat_input("Type your message...")
if user_input:
    # Append user message to history
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("👤"):
        st.write(user_input)  # Show input immediately

    user_message = HumanMessage(content=user_input)
    user_message.pretty_print()

    # Stream response from agent_workflow

    response_placeholder = st.empty()
    full_response = ""

    for step in agent_workflow.stream([user_message], config):
        for task_name, message in step.items():
            if isinstance(message, ToolMessage):
                continue
            if task_name == "agent_workflow":
                continue

            # Print bot response to console
            print(f"\n{task_name}:")
            message.pretty_print()

            # Display streamed response in UI
            full_response += message.content + "\n"
            response_placeholder.markdown(full_response.strip())

    # Append bot response to history
    st.session_state.chat_history.append(("assistant", full_response.strip()))
    st.rerun()  # Refresh UI with new messages
