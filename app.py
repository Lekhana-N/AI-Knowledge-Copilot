import streamlit as st
from models.llm import get_llm_response
from utils.rag import process_pdf, get_answer
from utils.web_search import search_web

# Title
st.title("AI Knowledge Copilot 🤖")

# Web search toggle
use_web = st.checkbox("Enable Web Search 🌐")

# Response mode
mode = st.radio(
    "Select Response Mode",
    ["Concise", "Detailed"]
)

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.session_state.vectorstore = process_pdf("temp.pdf")
    st.success("PDF processed successfully!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build conversation
    conversation = ""
    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Style instruction
    if mode == "Concise":
        style_instruction = "Give a short and clear answer in 3-4 lines."
    else:
        style_instruction = "Give a detailed explanation with examples."

    # Decide source
    if st.session_state.vectorstore:
        context = get_answer(st.session_state.vectorstore, user_input)
        prompt = f"""
        {style_instruction}

        Answer using the following document context:

        {context}

        Conversation:
        {conversation}

        Answer the latest question clearly.
        """

    elif use_web:
        web_result = search_web(user_input)
        prompt = f"""
        {style_instruction}

        Answer using this web data:

        {web_result}

        Conversation:
        {conversation}

        Answer the latest question clearly.
        """

    else:
        prompt = f"""
        {style_instruction}

        Conversation:
        {conversation}

        Answer the latest question.
        """

    # Get response
    response = get_llm_response(prompt)

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)