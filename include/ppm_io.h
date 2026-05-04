#pragma once

#include "buffer.h"

using GrayBuffer = FrameBuffer;

FrameBuffer read_ppm(const char* filename);
void write_ppm(const char* filename, GrayBuffer& buffer);
