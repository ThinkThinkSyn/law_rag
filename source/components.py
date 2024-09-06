import asyncio
from copy import deepcopy
import time
import streamlit as st
from loguru import logger

from .api_requests import submit_review


@st.dialog("Review")
def review_pop_up_dialog():
    st.write("Please leave a review for the chatbot.")

    # Options for submitting a review
    rating = st.slider("Rating", min_value=0, max_value=5)
    comment = st.text_area("Comment")
    submit_session_state = st.checkbox(
        "Submit chat history and configuration to improve our chatbot.",
        value=True
    )

    submit_button = st.button("Submit")
    if submit_button:
        try:
            # Preprocess session state as configuration to submit
            configuration_to_submit = None
            if submit_session_state:
                configuration_to_submit = deepcopy(st.session_state.to_dict())
                configuration_to_submit['config'].pop("api_access_key", None)
                logger.info(f"Submitting configuration: {str(configuration_to_submit)}")
                configuration_to_submit = str(configuration_to_submit)

            # Submit review
            asyncio.run(
                submit_review(
                    api_access_key=st.session_state.config["api_access_key"],
                    rating=rating,
                    comment=comment,
                    configuration=configuration_to_submit
                )
            )
            st.success("Review submitted successfully!")
            time.sleep(2)
            st.rerun()

        except Exception as e:
            st.error(f"Failed to submit review. Error: {str(e)}")

