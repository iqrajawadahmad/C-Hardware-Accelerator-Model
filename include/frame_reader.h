#pragma once
#include "pixel.h"
#include <string>

struct FrameReader{
    int w,h;
    int x,y;
    Pixel* frame;
    bool done;

    FrameReader(int W,int H,const std::string &filename="");
    ~FrameReader();
    Pixel next_pixel();
};

