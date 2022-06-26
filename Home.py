""" ---- DASHBOARD DS4A PROJECT ---- """

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome 👋")


if __name__ == "__main__":
    run()
