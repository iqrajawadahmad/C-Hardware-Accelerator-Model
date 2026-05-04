#pragma once
#include "buffer.h"

struct Smooth3x3{
    gray_t buf[3][3];
    Smooth3x3();
    gray_t next_pixel(gray_t in);
};
