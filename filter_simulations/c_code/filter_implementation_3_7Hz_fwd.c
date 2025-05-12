#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dsps_biquad.h"
#include "esp_dsp.h"
#include "c_data.h"

// Example SOS for one biquad section (change as needed)
#define NUM_STAGES 4

float sos_bp[NUM_STAGES][5] = {
    {0.0031060479,-0.0061745703,0.0031060479,-1.9773009389,0.9775540479},
    {1.0000000000,-1.9977658930,1.0000000000,-1.9902530538,0.9906638595},
    {1.0000000000,-1.9999992277,1.0000000000,-1.9914215200,0.9914579192},
    {1.0000000000,-1.9999958136,1.0000000000,-1.9977812778,0.9978039242}
};


float temp[NUM_SAMPLES];    // For intermediate results
float temp2[NUM_SAMPLES];
float output[NUM_SAMPLES];  // Final output

float biquad_state_forward[4 * NUM_STAGES];
float biquad_state_backward[4 * NUM_STAGES];

void apply_sosfiltfilt(float sos[][5], int num_stages, float *x, float *y, int len) {
    memcpy(temp, x, sizeof(float) * len);

    // Forward pass
    memset(biquad_state_forward, 0, sizeof(biquad_state_forward));
    for (int i = 0; i < num_stages; i++) {
        dsps_biquad_f32_aes3(temp, temp, len,
            sos[i],
            &biquad_state_forward[4 * i]);
    }

    memcpy(y, temp, sizeof(float) * len);
}

void print_output(float *arr, int len) {
    for (int i = 0; i < len; i++) {
        printf("%f\n", arr[i]);
    }
}

void app_main() {
    apply_sosfiltfilt(sos_bp, NUM_STAGES, input, output, NUM_SAMPLES);
    print_output(output, NUM_SAMPLES);
}