import streamlit as st
import requests
import time

# Update with your actual FastAPI backend URL if different
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AUTOSAR AI Assistant", layout="wide")

st.title("Automotive Engineering AI")
st.subheader("Case Study 1: AUTOSAR HLD Document Analysis Assistant")

st.sidebar.header("Configuration")
st.sidebar.info("API Key is securely configured in the backend.")

st.sidebar.header("Document Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload AUTOSAR HLD PDF", type=["pdf"])

if st.sidebar.button("Process Document"):
    if not uploaded_file:
        st.sidebar.error("Please upload a PDF first.")
    else:
        with st.spinner("Extracting text and generating embeddings..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                if response.status_code == 200:
                    st.sidebar.success(response.json().get("message", "Document processed!"))
                else:
                    st.sidebar.error(f"Error processing document: {response.text}")
            except requests.exceptions.ConnectionError:
                st.sidebar.error("Backend server is not running. Please start FastAPI.")

st.markdown("---")
st.markdown("### Architecture Question Answering")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about components, interfaces, dependencies..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing architecture knowledge base...")
        
        try:
            payload = {"query": prompt}
            response = requests.post(f"{BACKEND_URL}/query", json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer generated.")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"API Error: {response.text}"
                message_placeholder.error(error_msg)
        except requests.exceptions.ConnectionError:
            message_placeholder.error("Backend server is not running. Please start FastAPI.")
