""" ---- DASHBOARD DS4A PROJECT ---- """

import streamlit as st
from streamlit.logger import get_logger

#style
styl = f"""
<style>
  .css-1siy2j7 {{
    width: 10rem;
  }}
</style>
"""

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="HOME",
        page_icon="💡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(styl, unsafe_allow_html=True)
    st.write("# Welcome 👋")
    st.title('KIOSCOS VIVE DIGITAL - PRUEBAS SABER 11')

if __name__ == "__main__":
    run()
