#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "signal_proc_misc.h"
#include <stddef.h>


PeakFinder* init_peak_finder(uint_fast16_t fs, uint_fast16_t max_input_size) {
    PeakFinder* pf = (PeakFinder*)malloc(sizeof(PeakFinder));
    if (!pf) return NULL;

    pf->output = (int*)malloc(sizeof(int) * max_input_size);
    if (!pf->output) {
        free(pf);
        return NULL;
    }

    pf->output_size = max_input_size;
    pf->window_size = fs;
    if (pf->window_size > max_input_size)
        pf->window_size = max_input_size;

    return pf;
}

int* find_peaks(PeakFinder* pf, int* input, int h, uint_fast16_t size) {
    if (!pf || !input || !pf->output) return NULL;
    if (h == 0) h = 1;

    pf->sum_x = 0;
    pf->sum_x2 = 0;
    pf->start = 0;
    pf->end = pf->window_size;
    int arrIdx = 0;

    // Fill initial window
    for (int i = 0; i < pf->window_size; i++) {
        int val = input[i];
        pf->sum_x += val;
        pf->sum_x2 += (int64_t)val * val;
    }

    bool localPeak = false;
    int currIdx = 0;

    for (int i = 0; i < size - 1; i++) {
        if (i > pf->window_size / 2 && pf->end < size) {
            int remove_val = input[pf->start];
            int add_val = input[pf->end];
            pf->sum_x -= remove_val;
            pf->sum_x2 -= (int64_t)remove_val * remove_val;
            pf->sum_x += add_val;
            pf->sum_x2 += (int64_t)add_val * add_val;
            pf->start++;
            pf->end++;
        }

        int actual_window = pf->end - pf->start;
        int64_t mean_int = pf->sum_x / actual_window;

        // Compute std using float (only here)
        float mean = (float)pf->sum_x / actual_window;
        float mean_sq = mean * mean;
        float variance = ((float)pf->sum_x2 / actual_window) - mean_sq;
        float std = sqrtf(variance > 0 ? variance : 0);  // avoid sqrt(neg)

        if ((input[i] - mean_int) > h * std) {
            if (!localPeak) {
                localPeak = true;
                currIdx = i;
            } else if (input[i] > input[currIdx]) {
                currIdx = i;
            }
        } else if (localPeak) {
            localPeak = false;
            pf->output[arrIdx++] = currIdx;
        }
    }

    pf->output[arrIdx] = -1;
    return pf->output;
}