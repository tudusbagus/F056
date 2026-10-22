#include <iostream>
#include <cmath>
#include "Pythia8/Pythia.h"
#include <TFile.h>
#include <TTree.h>

using namespace Pythia8;

int main() {
    Pythia pythia;
    pythia.readFile("main_higgs.cmnd");
    pythia.init();
    int nEvents = pythia.mode("Main:numberOfEvents");
    TFile *outputFile = new TFile("higgs_mass.root", "RECREATE");
    TTree *tree = new TTree("events", "Arvore com eventos de producao do Higgs");
    double mH = 0.0;
    tree->Branch("mH", &mH, "mH/D");

    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (!pythia.next()) continue;
        int iHiggs = -1;
        for (int i = 0; i < pythia.event.size(); ++i) {
            if (pythia.event[i].id() == 25) iHiggs = i;
        }
        if (iHiggs != -1) {
            Vec4 pH(0.0, 0.0, 0.0, 0.0);
            int nDaughters = 0;
            bool isBbbar = false;
            for (int i = 0; i < pythia.event.size(); ++i) {
                if (pythia.event[i].mother1() == iHiggs) {
                    pH += pythia.event[i].p();
                    nDaughters++;
                    if (std::abs(pythia.event[i].id()) == 5) isBbbar = true;
                }
            }
            if (nDaughters > 0 && isBbbar) {
                mH = pH.mCalc();
                tree->Fill();
            }
        }
    }
    tree->Write();
    outputFile->Close();
    std::cout << "\n[SUCESSO] Sinal gerado!\n" << std::endl;
    return 0;
}
