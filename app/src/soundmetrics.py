from acoustic_toolbox import Signal
import soundscapy.audio as sa
import pandas as pd
import warnings

def res_to_df(res):
    return pd.DataFrame([dict(res.mean())])
def wavMetrics(wav):
    warnings.filterwarnings("ignore")
    s = Signal.from_wav(wav)
    if s.shape[0] == 2:
        df1 = sa.metrics.acoustics_metric_2ch(s, 'LAeq', as_df=True)
        df2 = sa.metrics.maad_metric_2ch(s, "all_spectral_alpha_indices", as_df=True)
        df1 = res_to_df(df1)
        df2 = res_to_df(df2)
    elif s.shape[0] != 2:
        df1 = sa.metrics.acoustics_metric_1ch(s, 'LAeq', as_df=True)
        df2 = sa.metrics.maad_metric_1ch(s, "all_spectral_alpha_indices", as_df=True)
        df1 = res_to_df(df1)
        df2 = res_to_df(df2)
    out = pd.concat([df1, df2], axis=1)
    # sa.metrics.mosqito_metric_2ch(s, "loudness_zwtv")
    return out