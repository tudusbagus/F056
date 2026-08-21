#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {
	if (argc < 2) {
		return 1;
	}
	int num = std::atoi(argv[1]);
	std::cout << "Hello world " << num << std::endl;
	return 0;
}
