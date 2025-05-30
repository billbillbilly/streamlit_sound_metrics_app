import streamlit as st

st.header("About")
st.markdown("""
This app extracts audio metrics from WAV files using the `soundscapy` python library.
It computes metrics like LAeq and spectral alpha indices.

### Instructions:
1. Set loacal directory/ Upload one or more WAV files.
2. Wait for the extraction to complete.
3. Download the results as a CSV file.

### Reference:
Mitchell, A., Aletta, F., & Kang, J. (2022). How to analyse and represent quantitative soundscape data. JASA Express Letters, 2, 37201. https://doi.org/10.1121/10.0009794
""")