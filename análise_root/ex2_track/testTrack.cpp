#include <iostream>
#include "Track.h"
#include "SimTrack.h"

int main() {
    Track recTrack(25.0, 1.2, 0.5, 1);
    SimTrack simTrack(25.5, 1.21, 0.49, 1, 13); // PDG 13 = Muon

    std::cout << "--- Track Reconstruido ---" << std::endl;
    std::cout << "Pt: " << recTrack.Pt() << " GeV | Eta: " << recTrack.Eta() 
              << " | Phi: " << recTrack.Phi() << " | Carga: " << recTrack.Charge() << std::endl;
    std::cout << "Px: " << recTrack.Px() << " | Py: " << recTrack.Py() 
              << " | Pz: " << recTrack.Pz() << " | P: " << recTrack.P() << std::endl;

    std::cout << "\n--- SimTrack (Monte Carlo) ---" << std::endl;
    std::cout << "Pt: " << simTrack.Pt() << " GeV | PDG ID: " << simTrack.PdgId() << std::endl;

    return 0;
}
