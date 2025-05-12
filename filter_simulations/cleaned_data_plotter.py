import matplotlib.pyplot as plt
from optimal_filter_cheby import optimal_filter_cheby 
from scipy.fft import fft, fftfreq
import numpy as np
from scipy.signal import butter, cheby2, sosfilt_zi, sosfilt, sosfiltfilt, kaiserord, lfilter, firwin, freqz, find_peaks

# input_file = '10-08-2024-14-55-43 trial no 1 cleaned.txt'
input_file = '10-08-2024-15-30-18 trial no 7 cleaned.txt'

def flatten(xss):
    return [x for xs in xss for x in xs]

def parse_adc_values(hex_string, max_value=1.2):
    # Convert the hex string to an integer
    num = int(hex_string, 16)

    # Ignore the first two binary bits
    num &= 0x3FFFFF
    bits = 22

    # If the highest bit (bit 20) is set, calculate the two's complement
    if (num & (1 << (bits - 1))) != 0:
        num = num - (1 << bits)
    # if num & (1 << 20):
    #     num -= 1 << 21

    if max_value:
        unit_voltage = max_value/(2**(bits-1))
        num = num * unit_voltage
    return num


def parse_raw_data(input_file):
    afe1_led1 = []
    afe1_led2 = []
    afe1_led3 = []
    afe1_led4 = []

    afe2_led1 = []
    afe2_led2 = []
    afe2_led3 = []
    afe2_led4 = []
    
    with open(input_file, 'r') as f:
        content = f.readlines()

        afe_no = content
        for line in content:
            for i in range(0, len(line)//24):
                afe_no = line[2:4]
                line = line[4:]

                if afe_no == '01':
                    afe1_led2.append(parse_adc_values(line[24*i+0:24*i+6]))
                    afe1_led3.append(parse_adc_values(line[24*i+6:24*i+12]))
                    afe1_led1.append(parse_adc_values(line[24*i+12:24*i+18]))
                    afe1_led4.append(parse_adc_values(line[24*i+18:24*i+24]))
                elif afe_no == '02':
                    afe2_led2.append(parse_adc_values(line[24*i+0:24*i+6]))
                    afe2_led3.append(parse_adc_values(line[24*i+6:24*i+12]))
                    afe2_led1.append(parse_adc_values(line[24*i+12:24*i+18]))
                    afe2_led4.append(parse_adc_values(line[24*i+18:24*i+24]))
    
    return (afe1_led1, afe1_led2, afe1_led3, afe1_led4,
            afe2_led1, afe2_led2, afe2_led3, afe2_led4)

if __name__ == "__main__":
        
    afe1_led1 = []
    afe1_led2 = []
    afe1_led3 = []
    afe1_led4 = []

    afe2_led1 = []
    afe2_led2 = []
    afe2_led3 = []
    afe2_led4 = []

    # Parse the data header first
    with open(input_file, 'r') as f:
        content = f.readlines()

        afe_no = content
        for line in content:
            for i in range(0, len(line)//24):
                afe_no = line[2:4]
                line = line[4:]

                if afe_no == '01':
                    afe1_led2.append(parse_adc_values(line[24*i+0:24*i+6]))
                    afe1_led3.append(parse_adc_values(line[24*i+6:24*i+12]))
                    afe1_led1.append(parse_adc_values(line[24*i+12:24*i+18]))
                    afe1_led4.append(parse_adc_values(line[24*i+18:24*i+24]))
                elif afe_no == '02':
                    afe2_led2.append(parse_adc_values(line[24*i+0:24*i+6]))
                    afe2_led3.append(parse_adc_values(line[24*i+6:24*i+12]))
                    afe2_led1.append(parse_adc_values(line[24*i+12:24*i+18]))
                    afe2_led4.append(parse_adc_values(line[24*i+18:24*i+24]))

        fig, axs = plt.subplots(4, sharex=True)
        
        afe1_led1_filtered = optimal_filter_cheby(afe1_led1, 1000, 10, 0.35, True, True, False)
        afe1_led2_filtered = optimal_filter_cheby(afe1_led2, 1000, 10, 0.35, True, True, False)
        afe1_led3_filtered = optimal_filter_cheby(afe1_led3, 1000, 10, 0.35, True, True, False)
        afe1_led4_filtered = optimal_filter_cheby(afe1_led4, 1000, 10, 0.35, True, True, False)
        afe2_led1_filtered = optimal_filter_cheby(afe2_led1, 1000, 10, 0.35, True, True, False)
        afe2_led2_filtered = optimal_filter_cheby(afe2_led2, 1000, 10, 0.35, True, True, False)
        afe2_led3_filtered = optimal_filter_cheby(afe2_led3, 1000, 10, 0.35, True, True, False)
        afe2_led4_filtered = optimal_filter_cheby(afe2_led4, 1000, 10, 0.35, True, True, False)
        
        
        # Plot data
        line1, = axs[0].plot(afe1_led1, label='finger')
        line2, = axs[1].plot(afe1_led2, label='finger')
        line3, = axs[2].plot(afe1_led3, label='finger')
        line4, = axs[3].plot(afe1_led4, label='finger')

        line5, = axs[0].plot(afe2_led1, label='wrist')
        line6, = axs[1].plot(afe2_led2, label='wrist')
        line7, = axs[2].plot(afe2_led3, label='wrist')
        line8, = axs[3].plot(afe2_led4, label='wrist')

        line9, = axs[0].plot(afe1_led1_filtered*300, label='finger filtered')
        line10, = axs[1].plot(afe1_led2_filtered, label='finger filtered')
        line11, = axs[2].plot(afe1_led3_filtered, label='finger filtered')
        line12, = axs[3].plot(afe1_led4_filtered, label='finger filtered')
        
        line13, = axs[0].plot(afe2_led1_filtered, label='wrist filtered')
        line14, = axs[1].plot(afe2_led2_filtered, label='wrist filtered')
        line15, = axs[2].plot(afe2_led3_filtered, label='wrist filtered')
        line16, = axs[3].plot(afe2_led4_filtered, label='wrist filtered')

        # Add a single legend for the entire figure
        fig.legend([line1, line5, line9, line13,], labels=['finger', 'wrist', 'finger filtered', 'wrist filtered'], loc='upper right')

        plt.show()
