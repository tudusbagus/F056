CXX = g++
CXXFLAGS = -Wall -O2 -fPIC

all: testMET

libSimpleMET.so: SimpleMET.cpp SimpleMET.h
	$(CXX) $(CXXFLAGS) -shared SimpleMET.cpp -o libSimpleMET.so

testMET: testtMET.cpp libSimpleMET.so
	$(CXX) $(CXXFLAGS) testtMET.cpp ./libSimpleMET.so -Wl,-rpath,. -o testMET

clean:
	rm -f *.o *.so testMET
