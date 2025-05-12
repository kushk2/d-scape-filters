#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dsps_biquad.h"
#include "esp_dsp.h"
#include "c_data.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define NUM_STAGES 4
#define BATCH_SIZE 32
#define NUM_BATCHES (NUM_SAMPLES / BATCH_SIZE)

//rs = 70, lp_cutoff = 13.5
float sos_bp[NUM_STAGES][5] = {
    {0.0003129247,-0.0006112987,0.0003129247,-1.9772295223,0.9775851136},
    {1.0000000000,-1.9916405300,1.0000000000,-1.9882073712,0.9883036657},
    {1.0000000000,-1.9999992595,1.0000000000,-1.9888538885,0.9894718103},
    {1.0000000000,-1.9999958413,1.0000000000,-1.9967689980,0.9968249809},
};


float output[NUM_SAMPLES];  // Final output
float biquad_state[4 * NUM_STAGES];  // Persistent state between batches

void apply_sos_batch(float sos[][5], int num_stages, float *x, float *y, int len) {
    memcpy(y, x, sizeof(float) * len);  // copy input to output buffer
    for (int i = 0; i < num_stages; i++) {
        dsps_biquad_f32_aes3(y, y, len, sos[i], &biquad_state[4 * i]);
    }
}

void app_main() {
    vTaskDelay(1000/portTICK_PERIOD_MS);  // Delay to allow for system initialization

    memset(biquad_state, 0, sizeof(biquad_state));  // clear filter state

    for (int b = 0; b < NUM_BATCHES; b++) {
        int offset = b * BATCH_SIZE;
        float *batch_in = &input[offset];
        float *batch_out = &output[offset];

        int64_t t1 = esp_timer_get_time();  // start time
        apply_sos_batch(sos_bp, NUM_STAGES, batch_in, batch_out, BATCH_SIZE);
        int64_t t2 = esp_timer_get_time();  // end time

        printf("Batch %d took %lld us\n", b, (t2 - t1));
    }

   //Optional: print final output
    for (int i = 0; i < NUM_SAMPLES; i++) {
        printf("%f\n", output[i]);
    }
}