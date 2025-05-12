#ifndef signal_proc_misc_h
#define signal_proc_misc_h

#include <stdint.h>
#include <stdbool.h>
#include <math.h>

// Struct(s)
typedef struct {
    int* output;
    uint_fast16_t output_size;

    int64_t sum_x;
    int64_t sum_x2;

    uint_fast16_t window_size;
    int start;
    int end;
} PeakFinder;

// Function(s)
int* find_peaks(PeakFinder* pf, int* input, int h, uint_fast16_t size);
PeakFinder* init_peak_finder(uint_fast16_t fs, uint_fast16_t max_input_size);

#endif