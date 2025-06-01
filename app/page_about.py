import streamlit as st

st.header("About")
st.markdown("""
This app extracts audio metrics from WAV files using the `soundscapy` python library (Mitchell et al., 2022).
It computes and visualizes acoustic metrics like sound level, Acoustic Complexity Index, and etc.

### Instructions:
1. Set loacal directory/ Upload one or more WAV files.
2. Wait for the extraction to complete.
3. Download the results as a CSV file.
            
##### note:
To load data from your loacal directory, you need to clone this [repo](https://github.com/billbillbilly/streamlit_sound_metrics_app.git) and run the app in a local environment.

### Metrics:
- **LAeq**: A-weighted equivalent continuous sound level.
- **LAeq_5**: A-weighted equivalent continuous sound level over 5 seconds.
- **LAeq_10**: A-weighted equivalent continuous sound level over 10 seconds.
- **LAeq_50**: A-weighted equivalent continuous sound level over 50 seconds.
- **LAeq_90**: A-weighted equivalent continuous sound level over 90 seconds.
- **LAeq_95**: A-weighted equivalent continuous sound level over 95 seconds.
- **LAeq_max**: Maximum A-weighted equivalent continuous sound level.
- **LAeq_min**: Minimum A-weighted equivalent continuous sound level.
- **LAeq_kurt**: Kurtosis of the A-weighted equivalent continuous sound level.
- **LAeq_skew**: Skewness of the A-weighted equivalent continuous sound level.
- **MEANf**: Mean frequency of the sound - the average frequency of a sound signal weighted by its spectral energy distribution. It tells you where the center of mass of the spectrum lies.
- **VARf**: Variance of the frequency of the sound - the spread or dispersion of spectral energy around the mean frequency (MEANf). It is the second central moment of the frequency distribution, giving insight into how broad or narrow the spectrum is.
- **SKEWf**: Skewness of the frequency of the sound - the asymmetry of the spectral energy distribution relative to the mean frequency (MEANf). It tells you whether the energy is skewed toward lower or higher frequencies in a recording.
- **KURTf**: Kurtosis of the frequency of the sound - the peakedness or tailedness of the spectral energy distribution around the mean frequency (MEANf). It describes how concentrated or spread out the energy is across the frequency spectrum — especially relative to the spectral variance.
- **NBPEAKS**: Number of peaks in the sound - the number of distinct peaks in the frequency spectrum of a recording — typically based on the long-term average spectrum or LEQf curve.
- **LEQf**: Frequency-Based Equivalent Continuous Sound Level - the average acoustic energy (in dB) in each frequency bin over the duration of a recording. It is a frequency-resolved version of the overall Leq (Equivalent Continuous Sound Level).
- **ENRf**: Frequency-Based Envelope-to-Noise Ratio - the clarity or prominence of amplitude modulation (envelope) in each frequency bin, relative to its noise floor — providing insight into signal detectability in complex soundscapes.
- **BGNf**: Background Noise per Frequency Bin - the baseline or background energy level in each frequency bin, typically representing the lower envelope of the long-term spectrum.
- **SNRf**: Signal-to-Noise Ratio in each frequency bin - the clarity or strength of the signal relative to the background noise for each frequency bin across a recording.
- **Hf**: Spectral Entropy -  the entropy (randomness or unpredictability) of the frequency distribution in a sound signal.
- **EAS**: Equivalent Absorption Surface - a derived metric used to represent the total sound absorption capacity of a room or environment as if it were a single uniformly absorbing surface.
- **ECU**: Envelope Complexity Unit - an acoustic complexity metric derived from the amplitude envelope of the audio signal.
- **ECV**: Envelope Coefficient of Variation - the coefficient of variation (CV) of the amplitude envelope of the audio signal.
- **EPS**: Envelope Power Spectrum - a measure of the frequency distribution of amplitude fluctuations over time.
- **ACI**: Acoustic Complexity Index - the temporal variability of sound intensity within frequency bands — it's designed to capture rapid amplitude fluctuations that are typical of biological sounds like bird calls and insect chirps.
- **NDSI**: Normalized Difference Soundscape Index - the balance between biophonic and anthropophonic acoustic energy, providing a single value that reflects the relative dominance of natural (biological) vs. human-made noise in a recording.
- **rBA**: Relative Background Amplitude - the relative level of background sound in a recording, by comparing quieter portions of the signal to the overall amplitude.
- **AnthroEnergy**: Anthropogenic Acoustic Energy - the portion of acoustic energy in a recording that is likely due to anthropogenic (human-made) sources, such as vehicles, airplanes, construction, or other mechanical noise.  
- **BioEnergy**: Biophonic Acoustic Energy - the acoustic energy attributable to biological (non-human, non-geophysical) sources, such as birdsong, insects, amphibians, or mammals.
- **BI**: Bioacoustic Index - a measure of the acoustic activity and richness in specific frequency bands typically associated with biological sounds — especially birds, insects, and amphibians.
- **ROU**: Roughness - the temporal granularity or variability of the amplitude envelope — in other words, how "rough" or "choppy" the sound is over time.
- **ADI**: Acoustic Diversity Index - the distribution of acoustic energy across frequency bands, based on the assumption that greater biodiversity produces sounds across a wider range of frequencies.
- **AEI**: Acoustic Evenness Index - the evenness of acoustic energy distribution across frequency bands — it is a complement to the Acoustic Diversity Index (ADI), focusing on dominance vs. balance.
- **LFC**: Low-Frequency Cover - the proportion of time during which low-frequency bands are acoustically active.
- **MFC**: Mid-Frequency Cover - the percentage of time that mid-frequency bands are acoustically active. 
- **HFC**: High-Frequency Cover - the percentage of time that high-frequency bands are acoustically active.
- **ACTspFract**: Active Spectral Fraction - the proportion of frequency bins (across the spectrum) that are active.   
- **ACTspCount**: Active Spectral Count - the number of frequency bins that are active.
- **ACTspMean**: Active Spectral Mean - the mean value of active frequency bins.
- **EVNspFract**: Even Spectral Fraction - the proportion of frequency bins where the spectral energy is uniform or evenly distributed across the spectrum.
- **EVNspMean**: Even Spectral Mean - the mean value of evenly distributed frequency bins.
- **EVNspCount**: Even Spectral Count - the number of frequency bins that are evenly distributed.
- **TFSD**: Time-Frequency Signal Diversity - the diversity of acoustic activity across both time and frequency domains — capturing how rich and variable a soundscape is in its time–frequency structure.
- **H_Havrda**: Havrda–Charvát Entropy - a generalized entropy measure that extends the classical Shannon entropy to allow for tunable sensitivity to rare or dominant events.
- **H_Renyi**: Renyi Entropy - a family of entropy measures that generalizes Shannon entropy, allowing for different sensitivity to the distribution of probabilities.
- **H_pairedShannon**: Paired Shannon Entropy - a measure of uncertainty that accounts for paired observations, often used in ecological and environmental data.
- **H_gamma**: Gamma Entropy - a measure of uncertainty that is sensitive to the distribution of probabilities, particularly in ecological contexts.
- **H_GiniSimpson**: Gini-Simpson Index - a measure of diversity that accounts for both richness and evenness in a community, often used in ecology.
- **RAOQ**: Rao’s Quadratic Entropy - a measure of acoustic diversity that considers both the relative abundance of sounds (e.g., energy in frequency bins) and their dissimilarity — typically across the frequency spectrum.
- **AGI**: Acoustic General Index - the overall acoustic activity or richness in a recording by integrating multiple acoustic features, often from the spectrogram.
- **nROI**: Number of Regions of Interest - the number (or normalized count) of Regions of Interest (ROIs) in the time–frequency space of an audio recording that are above a defined energy threshold, and often meet criteria for duration and frequency range.
- **aROI**: Average Region of Interest - the average acoustic energy or activity within the Regions of Interest (ROIs) in the time–frequency space of an audio recording.
            
### Reference:
Mitchell, A., Aletta, F., & Kang, J. (2022). How to analyse and represent quantitative soundscape data. JASA Express Letters, 2, 37201. https://doi.org/10.1121/10.0009794
""")