import streamlit as st
import pandas as pd
from tqdm import tqdm
import src.soundmetrics as soundmetrics
import plotly.figure_factory as ff
import plotly.graph_objects as go
import os

# def plot_metrics(df):
#     """Plot audio metrics."""
#     metrics = df.columns.tolist()
#     metrics.pop(-1)
#     hist_data = [df[metrics[i]].tolist() for i in range(len(metrics))]

#     if not hist_data:
#         st.warning("No metrics available to plot.")
#         return None
#     return ff.create_distplot(hist_data, metrics, bin_size=0.2, show_hist=False, show_rug=False)

def plot_metrics(df):
    """Plot audio metrics over index."""
    metrics = df.columns.tolist()
    metrics.pop(0)
    metrics.pop(-1)

    fig = go.Figure()

    for metric in metrics:
        fig.add_trace(go.Scatter(
            x=df.file_name,
            y=df[metric],
            mode='lines+markers',
            name=metric
        ))

    fig.update_layout(
        title="Audio Metrics Over Index",
        xaxis_title="Audio File",
        yaxis_title="Metric Value",
        template="plotly_dark",
        xaxis=dict(
            tickangle=90  # or 90, -45, etc.
        ),
    )

    return fig

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
        results = None
        # Load .wav files from the directory
        files = {f: os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith('.wav')}
        
        st.write(f"Found {len(files)} .wav files in the directory.")

        if st.button("Extract Audio Metrics"):
            with st.spinner("Processing audio files..."):
                for f_name, wav_path in tqdm(files.items()):
                    try:
                        result = soundmetrics.wavMetrics(wav_path)
                        result['file_name'] = f_name

                        if results is None:
                            results = result
                        else:
                            results = pd.concat([results, result])
                            results = results.reset_index()
                    except Exception as e:
                        st.warning(f"Failed to process {f_name}: {e}")

            if results is not None:
                st.success("Extraction complete!")
                st.dataframe(results)

                # Allow download
                csv = results.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv", key="extract_metrics1")
                fig = plot_metrics(results)
                if fig:
                    st.plotly_chart(fig, key="plot_metrics1")
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

                    with open(file_name, 'wb') as f:
                        f.write(file.read())
                    
                    result = soundmetrics.wavMetrics(file_name)
                    result['file_name'] = file_name
                    
                    if results is None:
                        results = result
                    else:
                        results = pd.concat([results, result])
                        results = results.reset_index()
                    os.remove(file_name)
                except Exception as e:
                    st.warning(f"Failed to process {file.name}: {e}")

        if results is not None:
            st.success("Extraction complete!")
            st.dataframe(results)

            # Download CSV
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "audio_metrics.csv", "text/csv", key="extract_metrics2")

            fig = plot_metrics(results)
            if fig:
                st.plotly_chart(fig, key="plot_metrics2")