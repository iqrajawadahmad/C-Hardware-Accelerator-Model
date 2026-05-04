#pragma once
#include <cstring>
struct DMA{
    static void transfer(void* src, void* dst,int size){
#ifdef ENABLE_DMA
        memcpy(dst,src,size);
#endif
    }
};
