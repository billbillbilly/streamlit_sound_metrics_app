import streamlit as st

st.title("Audio Metrics Extractor")

with st.sidebar:
    app_page = st.Page("page_app.py", title="Metrics Extractor", icon=":material/equalizer:")
    about_page = st.Page("page_about.py", title="About", icon=":material/home:")

pg = st.navigation([app_page, about_page])
pg.run()
