#include "smoothing_filter.h"

Smooth3x3::Smooth3x3(){
    for(int i=0;i<3;i++)
        for(int j=0;j<3;j++) buf[i][j]=0;
}

gray_t Smooth3x3::next_pixel(gray_t in){
    // shift pixels
    buf[0][0]=buf[0][1]; buf[0][1]=buf[0][2]; buf[0][2]=in;
    buf[1][0]=buf[1][1]; buf[1][1]=buf[1][2]; buf[1][2]=buf[0][2];
    buf[2][0]=buf[2][1]; buf[2][1]=buf[2][2]; buf[2][2]=buf[1][2];

    int sum=0;
    for(int i=0;i<3;i++)
        for(int j=0;j<3;j++)
            sum += buf[i][j];

    return sum/9;
}
