import streamlit as st
import pandas as pd
from tqdm import tqdm
import src.soundmetrics as soundmetrics
import plotly.graph_objects as go
import os

@st.cache_data
def extract_metrics_from_upload(file_list) -> pd.DataFrame:
    results = []
    for file in file_list:
        try:
            file_name = file.name
            with open(file_name, 'wb') as f:
                f.write(file.read())

            result = soundmetrics.wavMetrics(file_name)
            result['file_name'] = file_name
            results.append(result)

            os.remove(file_name)
        except Exception as e:
            st.warning(f"Failed to process {file.name}: {e}")
    if results:
        df = pd.concat(results).reset_index(drop=True)
        df.drop(columns=[col for col in ['index', 'level_0'] if col in df.columns], inplace=True, errors='ignore')
        return df
    else:
        return pd.DataFrame()
    
@st.cache_data
def extract_metrics_from_directory(files: dict) -> pd.DataFrame:
    results = []
    for f_name, wav_path in files.items():
        try:
            result = soundmetrics.wavMetrics(wav_path)
            result['file_name'] = f_name
            results.append(result)
        except Exception as e:
            st.warning(f"Failed to process {f_name}: {e}")
    if results:
        df = pd.concat(results).reset_index(drop=True)
        df.drop(columns=[col for col in ['index', 'level_0'] if col in df.columns], inplace=True, errors='ignore')
        return df
    else:
        return pd.DataFrame()

def play_audio(file_path):
    """Play audio file in Streamlit."""
    if os.path.exists(file_path):
        audio_file = open(file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    else:
        st.error(f"File {file_path} does not exist.")

def plot_metrics(df, key=None):
    """Interactive plotting of selected audio metrics."""
    metrics = [col for col in df.columns if col != 'file_name']

    selected_metrics = st.multiselect(
        "Select metrics to plot",
        metrics,
        default=metrics,
        key=key
    )

    if selected_metrics:
        fig = go.Figure()
        for metric in selected_metrics:
            fig.add_trace(go.Scatter(
                x=df["file_name"],
                y=df[metric],
                mode='lines+markers',
                name=metric
            ))

        fig.update_layout(
            title="Selected Audio Metrics",
            xaxis_title="Audio File",
            yaxis_title="Metric Value",
            template="plotly_dark",
            xaxis=dict(tickangle=90),
        )
        return fig
    else:
        st.info("Please select at least one metric to display.")

tab_upload_path, tab_dir_path = st.tabs(
    [
        "Upload Audio Files", 
        "Load Audio Directory",
    ]
)

with tab_dir_path:
    st.header("Load Audio Directory")
    if "results_dir" not in st.session_state:
        st.session_state.results_dir = None

    dir_path = st.text_input("Enter the path to your local audio directory", value="path/to/your/audio/files")
    if dir_path and os.path.exists(dir_path):
        # Load .wav files from the directory
        files = {f: os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith('.wav')}
        
        st.write(f"Found {len(files)} .wav files in the directory.")

        if st.button("Extract Audio Metrics"):
            with st.spinner("Processing audio files..."):
                st.session_state.results_dir = extract_metrics_from_directory(files)
                results = extract_metrics_from_directory(files)
    results = st.session_state.results_dir
    if results is not None and not results.empty:
        st.success("Extraction complete!")
        st.dataframe(results)

        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv", key="extract_metrics1")

        selected_audio = st.selectbox(
            "Audio Playlist",
            [*files],
            index=None,
            placeholder="Select a saved audio file to play",
            key="audio_playlist_dir"
        )
        if selected_audio:
            play_audio(files[selected_audio])

        if 'file_name' in results.columns and len(results.columns) > 1:
            fig = plot_metrics(results, key="plot_1")
            if fig:
                st.plotly_chart(fig, use_container_width=True, key="plot_metrics1")
        else:
            st.warning("No valid metrics to plot.")

with tab_upload_path:
    st.header("Upload Audio Files")

    uploaded_files = st.file_uploader("Upload WAV files", type=["wav"], accept_multiple_files=True)

    if uploaded_files:
        results = None
        with st.spinner("Extracting audio metrics..."):
            results = extract_metrics_from_upload(uploaded_files)
            st.session_state.results_upload = results

        if results is not None:
            st.success("Extraction complete!")
            st.dataframe(results)
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv", key="extract_metrics2")

            file_dict = {file.name: file for file in uploaded_files}
            selected_name = st.selectbox("Choose a file to play", list(file_dict.keys()))
            if selected_name:
                selected_file = file_dict[selected_name]
                st.audio(selected_file.read(), format='audio/wav')

            if 'file_name' in results.columns and len(results.columns) > 1:
                fig = plot_metrics(results, key="plot_2")
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key="plot_metrics2")
            else:
                st.warning("No valid metrics to plot.")