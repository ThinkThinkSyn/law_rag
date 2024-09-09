import asyncio
import streamlit as st
import time
from typing import Generator

from source.data_types import RagMethod, RagType, Language
from source.components import review_pop_up_dialog
from source.api_requests import request_law_rag_chat


def string_streaming_simulation(string: str, num_of_slices: int = 500, delay: float = 0.005) -> Generator[str, None, None]:
    """
    Simulate streaming of a string by yielding parts of it with delays.

    Args:
    string (str): The input string to stream.
    num_of_slices (int): The number of slices to divide the string into. Defaults to 500.
    delay (float): The delay between yields in seconds. Defaults to 0.005.

    Yields:
    str: Parts of the input string.
    """
    if len(string) <= num_of_slices:
        for char in string:
            yield char
            time.sleep(delay)
    else:
        slice_size = len(string) // num_of_slices
        for i in range(0, len(string), slice_size):
            yield string[i:i+slice_size]
            time.sleep(delay)


def create_chatbot_response(response: dict):
    assert all(key in response for key in ["retrieved", "response"])
    if len(response["retrieved"]) == 0:
        return response["response"]
    
    retrieved_laws = "\n".join(f"{i + 1}. {item}"
                                for i, item in enumerate(rag_chat_response['retrieved']))
    retrieved_law_place_holder = "檢索到的法律" if st.session_state.config['language'].startswith("zh") else "Retrieved Laws"
    response_place_holder = "回應" if st.session_state.config['language'].startswith("zh") else "Response"
    
    return f"{retrieved_law_place_holder}:  \n{retrieved_laws}\n\n{response_place_holder}:  \n{rag_chat_response['response']}" 


st.set_page_config(
    page_title="Legal Expression Chatbot Testing",
    page_icon="⚖️",
    initial_sidebar_state="expanded",
)

st.title("⚖️ Legal Expression Chatbot Testing")

# Side bar for rag chat configuration
with st.sidebar:
    st.title("RAG Chat Configuration")
    api_access_key = st.text_input("API Access Key", type="password")
    language = st.selectbox("Language", [l.value for l in Language])
    method = st.selectbox("Method", [m.value for m in RagMethod])
    rag_type = st.selectbox("RAG Type", [t.value for t in RagType])
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

    write_review_button = st.button("Write Review")
    if write_review_button:
        review_pop_up_dialog()
    

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
