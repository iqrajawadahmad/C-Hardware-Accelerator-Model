#include "convolution.h"
#include <cstdlib>

Sobel::Sobel(){
    for(int i=0;i<3;i++)
        for(int j=0;j<3;j++)
            buf[i][j]=0;
}

gray_t Sobel::next_pixel(gray_t in){
    // shift pixels
    buf[0][0]=buf[0][1]; buf[0][1]=buf[0][2]; buf[0][2]=in;
    buf[1][0]=buf[1][1]; buf[1][1]=buf[1][2]; buf[1][2]=buf[0][2];
    buf[2][0]=buf[2][1]; buf[2][1]=buf[2][2]; buf[2][2]=buf[1][2];

    int gx = buf[0][2]+2*buf[1][2]+buf[2][2] - buf[0][0]-2*buf[1][0]-buf[2][0];
    int gy = buf[2][0]+2*buf[2][1]+buf[2][2] - buf[0][0]-2*buf[0][1]-buf[0][2];

    int val = abs(gx)+abs(gy);
    if(val>255) val=255;
    return val;
}
