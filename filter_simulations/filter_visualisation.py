import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Suppose you already have your SOS:
sos = signal.cheby2(N=6, rs=50, Wn=[0.35, 10], btype='bandpass', fs=1000, output='sos')

# Frequency response
w, h = signal.sosfreqz(sos, worN=2000, fs=1000)

# Convert magnitude to dB
h_db = 20 * np.log10(np.maximum(np.abs(h), 1e-10))  # Avoid log(0)

plt.figure(figsize=(10, 5))
plt.plot(w, h_db)
plt.title('Frequency Response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude [dB]')
plt.grid(True)
plt.ylim(-100, 5)
plt.axhline(-80, color='r', linestyle='--', label='80 dB attenuation')
plt.legend()
plt.show()