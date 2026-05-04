#pragma once
#include "pixel.h"
#include <cstdlib>

struct FrameBuffer {
    int w,h;
    gray_t* pixels;
    FrameBuffer(): w(0), h(0), pixels(nullptr) {}
    FrameBuffer(int w_, int h_): w(w_), h(h_) {
        pixels = new gray_t[w*h];
    }
    ~FrameBuffer(){ delete[] pixels; }
    gray_t& at(int x,int y){ return pixels[y*w + x]; }
    gray_t* data(){ return pixels; }
    int width() const { return w; }
    int height() const { return h; }
};
