import asyncio
import streamlit as st
import time

from source.api_requests import request_law_rag_chat


def string_streaming_simulation(string: str):
    for char in string:
        yield char
        time.sleep(0.005)


def create_chatbot_response(response: dict):
    assert all(key in response for key in ["retrieved", "response"])
    if len(response["retrieved"]) == 0:
        return response["response"]
    
    retrieved_laws = "\n".join(f"{i + 1}. {item}"
                                for i, item in enumerate(rag_chat_response['retrieved']))
    retrieved_law_place_holder = "Retrieved Laws" if st.session_state.config['language'] == "en" else "檢索到的法律"
    response_place_holder = "Response" if st.session_state.config['language'] == "en" else "回應"
    return f"{retrieved_law_place_holder}:  \n{retrieved_laws}\n\n{response_place_holder}:  \n{rag_chat_response['response']}" 



st.title("⚖️ Legal Expression Chatbot")

# Side bar for rag chat configuration
with st.sidebar:
    st.title("RAG Chat Configuration")
    api_access_key = st.text_input("API Access Key", type="password")
    language = st.selectbox("Language", ["zh", "en"])
    method = st.selectbox("Method", ["DirectMatch", "ParentDoc", "NER", "HypoQuery"])
    rag_type = st.selectbox("RAG Type", ["Common", "Fusion"])
    top_k = st.number_input("Top K", value=5)
    parent_level = st.number_input("Parent Level", value=1)
    
    # Store the configuration in session state
    st.session_state.config = {
        "api_access_key": api_access_key,
        "language": language,
        "method": method,
        "rag_type": rag_type,
        "top_k": top_k,
        "parent_level": parent_level,
    }

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your legal question here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    response = None
    with st.chat_message("assistant"):
        try:
            rag_chat_response = asyncio.run(
                request_law_rag_chat(prompt, **st.session_state.config)
            )
            output = create_chatbot_response(rag_chat_response)
            response = st.write_stream(string_streaming_simulation(output))
        except Exception as e:
            st.error(str(e))

    # Add assistant response to chat history
    if response is not None:
        st.session_state.messages.append({"role": "assistant", "content": response})
