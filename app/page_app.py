import streamlit as st
import pandas as pd
from tqdm import tqdm
import src.soundmetrics as soundmetrics
import os

tab_dir_path, tab_upload_path = st.tabs(
    [
        "Load Audio Directory",
        "Upload Audio Files" 
    ]
)

with tab_dir_path:
    st.header("Load Audio Directory")

    dir_path = st.text_input("Enter the path to your local audio directory", value="path/to/your/audio/files")
    if dir_path and os.path.exists(dir_path):
        # Load .wav files from the directory
        files = {f: os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith('.wav')}
        
        st.write(f"Found {len(files)} .wav files in the directory.")

        if st.button("Extract Audio Metrics"):
            results = None
            with st.spinner("Processing audio files..."):
                for f_name, wav_path in tqdm(files.items()):
                    try:
                        result = soundmetrics.wavMetrics(wav_path)
                        result['file_name'] = f_name

                        if results is None:
                            results = result
                        else:
                            results = pd.concat([results, result])
                    except Exception as e:
                        st.warning(f"Failed to process {f_name}: {e}")

            if results is not None:
                st.success("Extraction complete!")
                st.dataframe(results)

                # Allow download
                csv = results.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv")
    else:
        st.warning("Please enter a valid directory path.")

with tab_upload_path:
    st.header("Upload Audio Files")
    
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