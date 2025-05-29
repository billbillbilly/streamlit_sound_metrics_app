import streamlit as st
import pandas as pd
from tqdm import tqdm
import src.soundmetrics as soundmetrics
import os

st.title("Audio Metrics Extractor")

# Upload audio files
uploaded_files = st.file_uploader("Upload WAV files", type=["wav"], accept_multiple_files=True)

if uploaded_files:
    results = None
    with st.spinner("Extracting audio metrics..."):
        for file in tqdm(uploaded_files):
            try:
                file_name = file.name
                # Save to a temp file
                with open(file_name, 'wb') as f:
                    f.write(file.read())
                
                # Extract metrics
                result = soundmetrics.wavMetrics(file_name)
                result['file_name'] = file_name
                
                if results is None:
                    results = result
                else:
                    results = pd.concat([results, result])
                    
                os.remove(file_name)  # Clean up
            except Exception as e:
                st.warning(f"Failed to process {file.name}: {e}")

    if results is not None:
        st.success("Extraction complete!")
        st.dataframe(results)

        # Download CSV
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv")