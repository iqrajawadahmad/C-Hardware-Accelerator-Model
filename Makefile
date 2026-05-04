CXX = g++

CXXFLAGS = -Wall -Wextra -std=c++17 -Iinclude

SRC = src/main.cpp \
      src/fsm.cpp \
      src/frame_reader.cpp \
      src/color_converter.cpp \
      src/smoothing_filter.cpp \
      src/convolution.cpp \
      src/output_writer.cpp \
      src/ppm_io.cpp

TARGET = accelerator
PROCESSOR = processor

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

processor: $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(PROCESSOR)

clean:
	rm -f $(TARGET) $(PROCESSOR)
# # Compiler
# CXX = g++

# # Compiler flags
# CXXFLAGS = -Wall -Wextra -std=c++17 -Iinclude

# # Source files
# SRC = src/main.cpp \
#       src/fsm.cpp \
#       src/frame_reader.cpp \
#       src/color_converter.cpp \
#       src/smoothing_filter.cpp \
#       src/convolution.cpp \
#       src/output_writer.cpp \
#       src/ppm_io.cpp

# # Output executable
# TARGET = accelerator
# PROCESSOR_WIN = processor.exe
# PROCESSOR_LINUX = processor

# # Default target
# all: $(TARGET)

# # Build rule
# $(TARGET): $(SRC)
# 	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

# # Build processor binary for distributed pipeline on Linux
# processor: $(PROCESSOR_LINUX)

# $(PROCESSOR_LINUX): $(SRC)
# 	$(CXX) $(CXXFLAGS) $(SRC) -o $(PROCESSOR_LINUX)

# # Build processor binary for Windows
# processor-win: $(PROCESSOR_WIN)

# $(PROCESSOR_WIN): $(SRC)
# 	$(CXX) $(CXXFLAGS) $(SRC) -o $(PROCESSOR_WIN)

# # Clean rule
# clean:
# 	rm -f $(TARGET) $(PROCESSOR_WIN) $(PROCESSOR_LINUX)
# # Rebuild from scratch

