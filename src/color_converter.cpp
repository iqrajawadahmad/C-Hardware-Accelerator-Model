#include "color_converter.h"

gray_t rgb2gray(const Pixel& p){
#ifdef USE_FIXED_POINT
    return (p.r*30 + p.g*59 + p.b*11)/100;
#else
    return (p.r+p.g+p.b)/3;
#endif
}
