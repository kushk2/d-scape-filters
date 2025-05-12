#include <stdio.h>
#include <string.h>
#include <math.h>
#include "data/c_data.h"

#include "lib/data_filters.h"
CHEBandPass* filter;

// #define NUM_SAMPLES 100       // Adjust to your signal length
#define SECTIONS 2            // Number of SOS sections
#define APPLY_HIGH_PASS 1     // 1 = apply high pass after low pass
#define INVERT_FLAG 1         // 1 = multiply final output by -1

float output[NUM_SAMPLES];
float input[NUM_SAMPLES];
int main() {

    // printf("Started\n");
    float output[NUM_SAMPLES];

    // printf("Create LP Filter \n");
    filter = create_che_band_pass_filter(4, 1.0f, 1000.0f, 0.35f, 10.0f);
    if(filter == NULL)
    {
        // printf("Failed to create filter\n");
        return 0;
    }
    // printf("Filter created\n");

    // Apply filter
    // printf("Apply filter\n");
    for(int i = 0; i < NUM_SAMPLES; i++) {
        output[i] = che_band_pass(filter, input[i]);
    }


    // Optional: invert signal
    if (1) {  // Set to 1 to invert
        for (int i = 0; i < NUM_SAMPLES; i++) {
            output[i] *= -1.0f;
        }
    }

    // Print output
    for (int i = 0; i < NUM_SAMPLES; i++) {
        printf("%f\n", output[i]);
    }

    return 0;
}