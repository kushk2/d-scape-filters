# Information about this folder (`filter_simulations`)

The main file in this folder is `chebyshev_comparison.py`. It builds upon `cleaned_data_plotter.py` by Yuting Xu, with the goal of being able to compile, modify and compare Chebyshev Type II filter implementations across both C and Python, acting as a verfication tool for this part of the signal processing pipeline.

Other saved data from experiments, filter coefficients, and iterations of

# `chebyshev_comparison.py`
## Main

Modify `input_file`, `python_output` and `c_output` variables accordingly to adjust which data/what file you are ingesting from, in terms of input data for the python filter, and for the `C`  implementation (if compiling), or `C` output file.

- `input_file`  points to raw (but cleaned) PPG data from a `Cleaned Data` folder. Note that results used `10-08-2024-14-55-43 trial no 1 cleaned.txt`
    - (https://imperiallondon-my.sharepoint.com/personal/yx8918_ic_ac_uk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fyx8918%5Fic%5Fac%5Fuk%2FDocuments%2FPhD%5FRA%2FTrials%2FCleaned%20Data&e=5%3A8f7930c58b3c4d7bb4cc03e5dc317da0&sharingv2=true&fromShare=true&at=9&CID=88be7167%2D762e%2D4ac6%2D930b%2D05533149313d&FolderCTID=0x01200044723EDB63580A459BE91FEB76C7AE74)
- `python_output()` which computes and stores the Python Chebyshev filter as specificied by the `optimal_filter_cheby.py` file (Yuting Xu).
- `c_output()`, which has two options:
    - `compute_c_chebyshev` provides a flag to compile the ANSI C implementation of the filter code and store the output in a Python object. 
    - `read_and_return` reads line seperated output data from a C filter. This is useful for running C implementation which utilises ESP-DSP directly on the ESP32 to test for correctness. 
- Both `python_output()` and `c_output()` contain options to plot, however to overlay the two, plotting code was migrated to main. Alongside the code that plots the raw, python and C output, is code to verify the length of the C code matches the Python code, as well as simliarity checks to see if the outputs yield within X order of magnitude. These checks are less applicable for ESP32 implementations where only a small segment of samples can be processed at once due to memory restrictions.
- Multiple helper functions are commented out such as saving filters, which can be toggled in and out accordingly to help with ease of implementing back and forth between a seperate platformio project 

## Helper Functions

- `save_filter_coeffs` creates a Chebyshev Type II filter and exports the Second Order Section (`sos`) coefficients to a txt file. This can be used in the C implementation via `biquadratic` multiplication operations.s
- `save_c_style` takes in a data input (from one led, for example, `afe1, led3`), and pads it with necessary information to be interpretable as a C array, this is needed for the ESP32 project and must be included in the relevant directories. This can be saved directly as a `.h` (header) file for ease of use.
- To create this input, use `parse_raw_data()` which has been slightly modified from the original (Yuting Xu) to parse raw hex data outputted from D-SCAPE v2, converting the fixed point hex into `double` floating point format data.


# `filter_visualisation.py`

Shows the frequency reponse of a filter. 

This was used to identify that expanding the low pass cutoff frequency of the bandpass filter greatly improved the rolloff properties by making the passband flatter for longer. This means that the dicrotic notch, which we still want to preserve, would be attenuated less significantly, whilst also eliminating more noise by promoting a sharper rolloff (acheived by increasing stopband attenuation). Note that an order 6 actually was ideal here but the ESP32/C implmenetation could not handle this, likely due to the lack precision (float rather than double for performance) causing errors to accumulate and leading to instability.
