CXX = g++
CXXFLAGS = -Wall -O2 -fPIC

all: testTrack

libTrack.so: Track.cpp Track.h SimTrack.cpp SimTrack.h
	$(CXX) $(CXXFLAGS) -shared Track.cpp SimTrack.cpp -o libTrack.so

testTrack: testTrack.cpp libTrack.so
	$(CXX) $(CXXFLAGS) testTrack.cpp ./libTrack.so -Wl,-rpath,. -o testTrack

clean:
	rm -f *.o *.so testTrack
