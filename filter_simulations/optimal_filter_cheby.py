import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal

def optimal_filter_cheby(data_signal, Fs, lp_cutoff, hp_cutoff, high_pass, invert_flag, smooth_SG, savgol_param=None):
    """
    Post processing (filtering) pipeline based on the optimal Chebyshev II filter
    :param data_signal: Array or dataframe of raw signal
    :param Fs: Sampling frequency (int)
    :param lp_cutoff: low-pass cutoff frequency (float)
    :param hp_cutoff: high-pass cutoff frequency (float)
    :param high_pass: True/False perform high pass filtering (bool)
    :param invert_flag: True/False perform signal inversion (bool)
    :param smooth_SG: True/False perform optimal SG smoothing (bool)
    :param savgol_param: (Optional) custom parameter to perfom SG smoothing if optimal is not desired (int/float)

    :returns: Filtered and post-rpocessed signal
    """
    Fn_f = int(Fs/2)
    sos_lp = signal.cheby2(4, 50,  lp_cutoff, 'lowpass', fs=Fs, output='sos')
    sos_hp = signal.cheby2(4, 50,  hp_cutoff, 'highpass', fs=Fs, output='sos')
    filtered_signal = signal.sosfiltfilt(sos_lp, data_signal)
    if high_pass:
        filtered_signal = signal.sosfiltfilt(sos_hp, filtered_signal)
    if invert_flag:
        filtered_signal *= -1
    if smooth_SG:
        #Find peak in frequency spectrum and calculate savgol parameter based on that 
        if savgol_param:
            savgol_param = (len(filtered_signal)/Fs)*2*savgol_param
            savgol_param = int(len(filtered_signal)/savgol_param)
            if savgol_param % 2 == 0:
                savgol_param -= 1
            #print(savgol_param)
            filtered_signal = signal.savgol_filter(filtered_signal, savgol_param, 3)
        else:
            if not high_pass:
                freq_val = obtain_peak_freq(signal.sosfiltfilt(sos_hp, filtered_signal), Fs)
            else:
                freq_val = obtain_peak_freq(filtered_signal, Fs)
            savgol_param = (len(filtered_signal)/Fs)*2*freq_val
            savgol_param = int(len(filtered_signal)/savgol_param)
            if savgol_param % 2 == 0:
                savgol_param -= 1
            #print(savgol_param)
            filtered_signal = signal.savgol_filter(filtered_signal, savgol_param, 3)

    return(filtered_signal)

def obtain_peak_freq(filtered_signal, Fs):
    data_y, data_x, _ = compute_FFT(len(filtered_signal), Fs, filtered_signal)
    #find peak in finger signal corresponding to HR
    peak_idx = np.argmax(np.abs(data_y))
    freq_val = data_x[peak_idx]
    return(freq_val)

def compute_FFT(N, fs, y):
    # sample spacing
    T = 1.0 / fs
    x = np.linspace(0.0, N*T, N, endpoint=False)
    yf = fft(y)
    xf = fftfreq(N, T)[:N//2]
    return(yf, xf, T)