#pragma once
#include "buffer.h"

struct Sobel{
    gray_t buf[3][3];
    Sobel();
    gray_t next_pixel(gray_t in);
};
