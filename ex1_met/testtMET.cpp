#include <iostream>
#include "SimpleMET.h"

int main() {
    SimpleMET met;

    std::cout << "--- Estado Inicial ---" << std::endl;
    std::cout << "Ex: " << met.Ex() << " | Ey: " << met.Ey() 
              << " | Modulo: " << met.Value() << " | Phi: " << met.Phi() << std::endl;

    // Adiciona dois objetos visiveis
    met.Add(12.0, 23.0);
    met.Add(-7.0, 42.0);

    std::cout << "\n--- Apos Adicionar Objetos ---" << std::endl;
    std::cout << "Ex: " << met.Ex() << " | Ey: " << met.Ey() 
              << " | Modulo: " << met.Value() << " | Phi: " << met.Phi() << std::endl;

    // Cancela o MET acumulado
    met.Add(-met.Ex(), -met.Ey());

    std::cout << "\n--- Apos Cancelamento ---" << std::endl;
    std::cout << "Ex: " << met.Ex() << " | Ey: " << met.Ey() 
              << " | Modulo: " << met.Value() << std::endl;

    return 0;
}
