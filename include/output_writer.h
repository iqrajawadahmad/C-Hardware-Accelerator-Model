#pragma once
#include "pixel.h"
#include <string>

void init_output(const std::string &filename="output.pgm");
void write_pixel(unsigned char p);
void close_output();

