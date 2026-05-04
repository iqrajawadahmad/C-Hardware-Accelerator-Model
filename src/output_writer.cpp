#include "output_writer.h"
#include <fstream>
#include "config.h"
#include <cstdio>

static std::ofstream fout;

void init_output(const std::string &filename){
    fout.open(filename, std::ios::binary);
    fout << "P5\n" << IMAGE_W << " " << IMAGE_H << "\n255\n";
}

void write_pixel(unsigned char p){
    if(fout.is_open()) fout.put(p);
}

void close_output(){
    if(fout.is_open()) fout.close();
}   
