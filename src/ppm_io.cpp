#include "ppm_io.h"
#include <fstream>
#include <iostream>
#include <sstream>

// ----------------------
// Read PPM file (RGB, P6)
// ----------------------
FrameBuffer read_ppm(const char* filename)
{
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Cannot open file: " << filename << "\n";
        return FrameBuffer(); // empty
    }

    std::string line;
    std::getline(file, line);
    if (line != "P6") {
        std::cerr << "Unsupported format (only P6 RGB PPM)\n";
        return FrameBuffer();
    }

    // Skip comment lines
    while (std::getline(file, line)) {
        if (line[0] != '#') break;
    }

    std::istringstream wh(line);
    int width, height;
    wh >> width >> height;

    int maxval;
    file >> maxval;
    file.get(); // skip single whitespace/newline

    // Create FrameBuffer (constructor allocates RGB buffer)
    FrameBuffer fb(width, height);

    // Read RGB data
    file.read(reinterpret_cast<char*>(fb.data()), width*height*3);
    file.close();

    return fb;
}

// ----------------------
// Write PPM file (grayscale, P5)
// ----------------------
void write_ppm(const char* filename, GrayBuffer& buffer)
{
    std::ofstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Cannot open file: " << filename << "\n";
        return;
    }

    file << "P5\n" 
         << buffer.width() << " " 
         << buffer.height() << "\n255\n"; // P5 = grayscale

    file.write(reinterpret_cast<const char*>(buffer.data()), buffer.width()*buffer.height());
    file.close();
}
 