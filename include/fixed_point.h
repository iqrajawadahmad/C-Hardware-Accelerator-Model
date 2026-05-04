#pragma once

typedef int fixed_t;
#define FP_SHIFT 8
#define FP_SCALE (1 << FP_SHIFT)

inline fixed_t fx_mul(fixed_t a, fixed_t b) {
    return (a * b) >> FP_SHIFT;
}
