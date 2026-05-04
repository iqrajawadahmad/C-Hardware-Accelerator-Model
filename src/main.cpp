#include <cstdio>
#include <string>
#include "fsm.h"
#include "frame_reader.h"
#include "color_converter.h"
#include "smoothing_filter.h"
#include "convolution.h"
#include "output_writer.h"
#include "config.h"

int main(int argc, char* argv[]) {
    std::string input_filename = "input.ppm";
    std::string output_filename = "output.pgm";
    if (argc >= 2) input_filename = argv[1];
    if (argc >= 3) output_filename = argv[2];

    bool start = true;

    FrameReader reader(IMAGE_W, IMAGE_H, input_filename);
    Smooth3x3 smooth;
    Sobel sobel;

    // init output file
    init_output(output_filename);

    // calculate initial latency from filter windows
    int initial_latency = (3-1) + (3-1); // Smooth + Sobel
    int total_pixels = IMAGE_W * IMAGE_H;

    int clk = 0;  // total clock counter
    int pixels_processed = 0;  // processed pixels counter

    // run pipeline until total clocks reach pixels + initial latency
    while(clk < total_pixels + initial_latency) {
        clk++;  // increment clock

        Pixel p;
        gray_t g = 0, s = 0, e = 0;

        // only process pixel if input is not done
        if(!reader.done) {
            fsm_tick(start);
            start = false;

            p = reader.next_pixel();
            g = rgb2gray(p);
            s = smooth.next_pixel(g);
            e = sobel.next_pixel(s);

            write_pixel(e);
            pixels_processed++;
        }

        // optional: print per row for console visualization
        if(clk <= total_pixels && clk % IMAGE_W == 0) printf("\n");
    }

    close_output();

    printf("\nPixels processed: %d\n", pixels_processed);
    printf("Pipeline done in %d clocks (including %d cycles initial latency)\n",
           clk, initial_latency);

    return 0;
}
