#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dsps_biquad.h"
#include "esp_dsp.h"
#include "c_data.h"

// Example SOS for one biquad section (change as needed)
#define NUM_STAGES 2

float sos_hp[NUM_STAGES][5] = {
    {0.9931058320,-1.9862109607,0.9931058320,-1.9902354893,0.9902640928}, // b0, b1, b2, a0 (expected 1.0 so disregarded), a1, a2
    {1.0000000000,-1.9999958721,1.0000000000,-1.9959236281,0.9959557261} // b0, b1, b2, a1, a2
};

float sos_lp[NUM_STAGES][5] = {
    {0.0030861974,-0.0060897013,0.0030861974,-1.9533928802,0.9540421597}, // b0, b1, b2 , a1, a2
    {1.0000000000,-1.9953771197,1.0000000000, -1.9821486995,0.9827374780} // b0, b1, b2, a1, a2
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
    // Apply LP filter
    printf("Applying LP\n");
    apply_sosfiltfilt(sos_lp, NUM_STAGES, input, output, NUM_SAMPLES);

    printf("Applying HP\n");
    apply_sosfiltfilt(sos_hp, NUM_STAGES, input, output, NUM_SAMPLES);

    printf("\nHP Filtered Output:\n");
    print_output(output, NUM_SAMPLES);
}