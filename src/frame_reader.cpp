#include "frame_reader.h"
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <string>
#include <sstream>

FrameReader::FrameReader(int W,int H,const std::string &filename){
    w = W;
    h = H;
    x = 0;
    y = 0;
    done = false;

    frame = new Pixel[w*h];

    if(filename != "") {
        std::ifstream fin(filename, std::ios::binary);
        if(fin){
            std::string line;
            std::getline(fin, line);
            if(line != "P6"){ 
                std::cerr << "Only P6 PPM supported\n"; 
                exit(1); 
            }

            // skip comments
            do {
                std::getline(fin, line);
            } while(line[0] == '#');

            // read width & height
            int Wf, Hf;
            std::sscanf(line.c_str(), "%d %d", &Wf, &Hf);
            w = Wf; h = Hf;

            // maxval line
            std::getline(fin, line);

            // read pixel data
            for(int i=0; i<w*h; i++){
                unsigned char rgb[3];
                fin.read(reinterpret_cast<char*>(rgb), 3);
                frame[i].r = rgb[0];
                frame[i].g = rgb[1];
                frame[i].b = rgb[2];
            }
            fin.close();
            std::cout << "PPM P6 file loaded: " << w << "x" << h << "\n";
            return;
        } else {
            std::cout << "PPM file not found, using fallback image.\n";
        }
    }

    // fallback
    for(int i=0;i<w*h;i++){
        frame[i].r = i%256;
        frame[i].g = (i*2)%256;
        frame[i].b = (i*3)%256;
    }
}

FrameReader::~FrameReader(){ delete[] frame; }

Pixel FrameReader::next_pixel(){
    Pixel p = frame[y*w + x];
    x++;
    if(x==w){ x=0; y++; }
    if(y==h) done = true;
    return p;
}

