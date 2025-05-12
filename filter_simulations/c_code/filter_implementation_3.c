#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dsps_biquad.h"
#include "esp_dsp.h"
#include "c_data.h"

// Example SOS for one biquad section (change as needed)
#define NUM_STAGES 4

float sos_bp[NUM_STAGES][5] = {
    {0.0030880129,-0.0060980963,0.0030880129,-1.9643495329,0.9648544182},
    {1.0000000000,-1.9954229471,1.0000000000,-1.9850973948,0.9858600412},
    {1.0000000000,-1.9999992477,1.0000000000,-1.9903875273,0.9904245190},
    {1.0000000000,-1.9999958307,1.0000000000,-1.9974157700,0.9974406067}
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

    // Reverse
    for (int i = 0; i < len / 2; i++) {
        float tmp = temp[i];
        temp[i] = temp[len - 1 - i];
        temp[len - 1 - i] = tmp;
    }

    // Backward pass
    memset(biquad_state_backward, 0, sizeof(biquad_state_backward));
    for (int i = 0; i < num_stages; i++) {
        dsps_biquad_f32_aes3(temp, temp, len,
            sos[i],
            &biquad_state_backward[4 * i]);
    }

    // Reverse again
    for (int i = 0; i < len / 2; i++) {
        float tmp = temp[i];
        temp[i] = temp[len - 1 - i];
        temp[len - 1 - i] = tmp;
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