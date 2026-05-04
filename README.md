# FPGA-Based Image Processing Pipeline Simulator

## Overview
This project is a C++ simulation of a hardware-style image processing pipeline, inspired by how
FPGAs and SoC vision accelerators process image data in a streaming manner.

The design focuses on hardware thinking rather than software optimization, emphasizing
dataflow, pipelining, and clock-cycle behavior used in embedded vision systems.

---

## What This Simulator Does
- Reads an input PPM image pixel by pixel  
- Converts RGB pixels to grayscale  
- Applies a 3×3 smoothing filter to reduce noise  
- Applies Sobel edge detection  
- Writes the result as a PGM grayscale image  
- Tracks total pipeline clock cycles, including initial startup latency  

---

## Key Components
- **Frame Reader**  
  Sequentially streams image pixels, modeling DDR-style memory access  

- **Color Converter**  
  Converts RGB pixels to grayscale (supports fixed-point computation)  

- **Smooth3x3 Filter**  
  Uses line-buffered sliding windows, modeling BRAM-style buffering  

- **Sobel Filter**  
  Performs edge detection using a pipelined convolution approach  

- **FSM Control**  
  Controls pipeline activation and sequencing, similar to hardware FSMs  

- **Clock Counter**  
  Tracks total execution cycles, including pipeline fill latency  

- **Output Writer**  
  Writes processed pixels to a PGM image file  

---

## Design Highlights
- Hardware-style streaming pipeline
- Cycle-accurate clock counting
- Clear separation of control (FSM) and datapath
- Line buffers to model BRAM behavior
- DMA-style sequential data movement abstraction

- 1-pixel-per-clock throughput after initial latency.
- Modular and easy to extend for additional filters or stages.
## Initial Latency
- Calculated as the sum of window delays for filters:

int initial_latency = (smooth_window_size-1) + (sobel_window_size-1);


##Code Structure 
include/
    config.h
    frame_reader.h
    color_converter.h
    smoothing_filter.h
    convolution.h
    output_writer.h
    fsm.h
src/
    main.cpp
    frame_reader.cpp
    color_converter.cpp
    smoothing_filter.cpp
    convolution.cpp
    output_writer.cpp
    fsm.cpp
Makefile
input.ppm



##Input 
-Input: PPM image (e.g., input.ppm, 256x256 pixels)
P6
256 256
255

##Output
-Grayscale PGM image (output.pgm)
-xdg-open output.pgm

##Compilation
-make

##EXECUTION 
-./accelerator
-Pipeline done in 65540 clocks (including 4 cycles initial latency)
-Pixels processed: 65536

##TO SEE PGM IMAGE in JPG

-sudo apt update
-sudo apt install imagemagick

-convert output.pgm output.png
-xdg-open output.png

##Commands 
![](images/input.png)



## Input vs Output Comparison

| Input Image |  Final Output |
|------------ |---------------|
| ![](images/input.png) | ![](images/output.png) |
