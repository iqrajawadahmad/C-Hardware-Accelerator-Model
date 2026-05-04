#include "dma.h"

// DDR → BRAM
void dma_read(DMA& dma) {
    if (!dma.src || !dma.dst || dma.size == 0) return;

    for (size_t i = 0; i < dma.size; ++i)
        dma.dst[i] = dma.src[i];
}

// BRAM → DDR
void dma_write(DMA& dma) {
    if (!dma.src || !dma.dst || dma.size == 0) return;

    for (size_t i = 0; i < dma.size; ++i)
        dma.dst[i] = dma.src[i];
}
