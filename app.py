import streamlit as st
from models.llm import get_llm_response
from utils.rag import process_pdf, get_answer
from utils.web_search import search_web


st.title("AI Knowledge Copilot 🤖")

use_web = st.checkbox("Enable Web Search 🌐")


mode = st.radio(
    "Select Response Mode",
    ["Concise", "Detailed"]
)

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.session_state.vectorstore = process_pdf("temp.pdf")
    st.success("PDF processed successfully!")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    
    conversation = ""
    for msg in st.session_state.messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    
    if mode == "Concise":
        style_instruction = "Give a short and clear answer in 3-4 lines."
    else:
        style_instruction = "Give a detailed explanation with examples."

    
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

    
    response = get_llm_response(prompt)

    
    st.session_state.messages.append({"role": "assistant", "content": response})

    
    with st.chat_message("assistant"):
        st.markdown(response)
