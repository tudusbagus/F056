#include <iostream>
#include <cmath>
#include "Pythia8/Pythia.h"
#include <TFile.h>
#include <TTree.h>

using namespace Pythia8;

int main() {
    Pythia pythia;
    pythia.readFile("main_background.cmnd");
    pythia.init();
    int nEvents = pythia.mode("Main:numberOfEvents");
    TFile *outputFile = new TFile("background_mass.root", "RECREATE");
    TTree *tree = new TTree("events", "Arvore com eventos de Fundo");
    double mH = 0.0;
    tree->Branch("mH", &mH, "mH/D");

    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (!pythia.next()) continue;
        Vec4 pB1(0.0, 0.0, 0.0, 0.0), pB2(0.0, 0.0, 0.0, 0.0);
        int foundB = 0;
        for (int i = 0; i < pythia.event.size(); ++i) {
            if (std::abs(pythia.event[i].id()) == 5 && pythia.event[i].status() > 0) {
                if (foundB == 0) { pB1 = pythia.event[i].p(); foundB++; }
                else if (foundB == 1) { pB2 = pythia.event[i].p(); foundB++; break; }
            }
        }
        if (foundB == 2) {
            Vec4 pTotal = pB1 + pB2;
            mH = pTotal.mCalc();
            tree->Fill();
        }
    }
    tree->Write();
    outputFile->Close();
    std::cout << "\n[SUCESSO] Fundo gerado!\n" << std::endl;
    return 0;
}
