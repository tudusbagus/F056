CXX = g++
CXXFLAGS = -Wall -O2 -std=c++20

INCLUDES = -I$(CONDA_PREFIX)/include
LIBS     = -L$(CONDA_PREFIX)/lib -lpythia8 $(shell root-config --libs) -lz -ldl -lpthread

all: main_higgs

main_higgs: main_higgs.cc
	$(CXX) $(CXXFLAGS) $(INCLUDES) main_higgs.cc -o main_higgs $(LIBS)

clean:
	rm -f main_higgs *.root *.o
