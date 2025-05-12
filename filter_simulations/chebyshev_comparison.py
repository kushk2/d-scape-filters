# This script compares the Cheybshev filter implementations in Pythona and C to verify correctness
from cleaned_data_plotter import parse_raw_data, parse_adc_values
from optimal_filter_cheby import optimal_filter_cheby
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
from scipy import signal

#parse the raw data from the input file
def save_c_style(input, output_file):
    with open(output_file, "w") as f:
        f.write("#pragma once\n")
        f.write(f"#define NUM_SAMPLES {len(input)}\n")
        f.write("float input[NUM_SAMPLES] = {\n")
        for i, val in enumerate(input):
            f.write(f"    {val:.6f}f")
            if i != len(input) - 1:
                f.write(",\n")
        f.write("\n};\n")
        
    print("Wrote data to file: ", output_file)
    
def read_and_return(filename):
    # Read file and convert each line to a float
    with open(filename, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]
    
    return data

def save_filter(order=4, rs=80, lp_cutoff=13.5, hp_cutoff=0.35, Fs=1000, output_dir="filter_coeffs"):

    #########################################
    # Print SOS coefficients for Chebyshev II filter
    # for C implementation
    ############################################

    sos_lp = signal.cheby2(order, 50,  lp_cutoff, 'lowpass', fs=Fs, output='sos')
    sos_hp = signal.cheby2(order, 50,  hp_cutoff, 'highpass', fs=Fs, output='sos')
    sos_bandpass = signal.cheby2(
        N=order,              
        rs=rs,             # Stopband attenuation in dB
        Wn=[hp_cutoff, lp_cutoff],  # Bandpass range
        btype='bandpass',
        fs=Fs,
        output='sos'
    )
    np.savetxt(output_dir + "/sos_bandpass.txt", sos_bandpass, fmt='%.10f', delimiter=",")
    np.savetxt(output_dir + "/sos_lp.txt", sos_lp, fmt='%.10f', delimiter=",")
    np.savetxt(output_dir + "/sos_hp.txt", sos_hp, fmt='%.10f', delimiter=",")
    print("Saved SOS coefficients to files.")
    print("Params: ", "order=", order, "rs=", rs, "lp_cutoff=", lp_cutoff, "hp_cutoff=", hp_cutoff, "Fs=", Fs)
        

def compute_python_chebyshev(input_data, plot=False):
    filtered_afe1_led3 = optimal_filter_cheby(input_data, 1000, 10, 0.35, True, True, False)
    
    if plot:
        print("Plotting data...")
        # Plot the raw and filtered data
        plt.figure(figsize=(10, 6))
        plt.plot(input_data, label='Raw PPG Signal (AFE1 LED1)', color='b')
        plt.plot(filtered_afe1_led3, label='Filtered PPG Signal (AFE1 LED1)', color='r')
        
        # Add labels and title
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.title('Raw vs Filtered PPG Signal')
        plt.legend()

        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()
    
    return filtered_afe1_led3

def compute_c_chebyshev(compile=True, plot=False):
    if compile:
        compile_cmd = [
        "gcc",
        "c_code/filter_implementation_1.c",
        "lib/data_filters.c",
        "-o", "filter_test",
        "-lm"
        ]

        print("Compiling...")
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if compile_result.returncode != 0:
            print("Compilation failed:")
            print(compile_result.stderr)
            exit(1)

        print("Compiled successfully.")

    # Step 2: Run and capture output
    print("Running executable...")
    run_result = subprocess.run(["./filter_test"], capture_output=True, text=True)

    if run_result.returncode != 0:
        print("Execution failed:")
        print(run_result.stderr)
        exit(1)

    # Step 3: Process output (e.g., split lines)
    output_lines = run_result.stdout.strip().split("\n")
    print("Captured output:")
    # for line in output_lines:
    #     print(line)

    # Optional: Parse into float array if it's all numbers
    try:
        parsed_output = [float(line.split()[-1]) for line in output_lines if line.strip()]
        print(f"\nParsed {len(parsed_output)} output samples.")
    except Exception as e:
        print("Couldn't parse output to floats:", e)
       
    if plot:
        # Plot the values
        plt.plot(parsed_output, label='Filtered PPG Signal (C Implementation)', color='g')
        plt.xlabel("Sample index")
        plt.ylabel("Value")
        plt.title("Signal Plot from file.txt")
        plt.grid(True)
        plt.show()

    return parsed_output


    
if __name__ == "__main__":
    input_file = './data/10-08-2024-14-55-43 trial no 1 cleaned.txt'
    input_file = './data/10-04-2024-15-25-03 trial no 2 cleaned.txt'
    afe1_led1, afe1_led2, afe1_led3, afe1_led4, afe2_led1, afe2_led2, afe2_led3, afe2_led4 = parse_raw_data(input_file)
    
    # save_filter(order=4,rs=60, lp_cutoff=15, hp_cutoff=0.35, Fs=1000, output_dir="filter_coeffs")
    # save_c_style(afe1_led3[:25000], "data/c_data.h")
    # np.savetxt("data/afe1_led3.txt", afe1_led3, fmt='%.10f', delimiter=",")        # Use to check if the input given to the C implementation is the same as the one used in Python
    
    python_output = compute_python_chebyshev(afe1_led3, plot=False)                 # Use this to run the Python implementation, returns to 'python_output' object  
    # c_output = compute_c_chebyshev(compile=True,plot=False)                       # Use this to compile and run the C implementation, returns to 'c_output' object
    c_output = read_and_return("data/esp32_outputs/trial2_verifcation_13.5hz_rs70.txt")           # Use this to read the output from the C implementation (genereated via a separate PlatformIO project and ran on ESP32)
    
    ####### Generic tests and graphing for the two implementations #######
    # print("Python output len: ", len(python_output))
    # print("C output len: ", len(c_output))
    # print("Length match?", len(python_output) == len(c_output))
    # print("Length difference: ", len(python_output) - len(c_output))

    # print("Content match?", np.allclose(python_output, c_output, atol=1e-2))
    # print("Python Output: ", python_output[:10])
    # print("C Output: ", c_output[:10])
    
    plt.figure(figsize=(10, 6))
    plt.plot(c_output, label="C Chebyshev Filter", color="green", alpha=0.7)
    plt.plot(afe1_led3, label="Raw Data", color="blue", alpha=0.7)
    plt.plot(python_output, label="Python Chebyshev Filter", color="red", alpha=0.7)

    plt.title("Comparison of Python vs C Chebyshev Filter Implementations")
    plt.xlabel("Sample Index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    