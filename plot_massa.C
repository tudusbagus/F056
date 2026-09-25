#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLegend.h>

void plot_massa() {
    TFile *fSinal = TFile::Open("higgs_mass.root");
    TTree *tSinal = (TTree*)fSinal->Get("events");
    TFile *fFundo = TFile::Open("background_mass.root");
    TTree *tFundo = (TTree*)fFundo->Get("events");

    TCanvas *c1 = new TCanvas("c1", "Massa Reconstruida", 800, 600);
    TH1F *hSinal = new TH1F("hSinal", "Massa Reconstruida;Massa Invariante [GeV];Eventos Normalizados", 50, 60, 160);
    TH1F *hFundo = new TH1F("hFundo", "Fundo", 50, 60, 160);

    tSinal->Draw("mH >> hSinal", "mH > 0", "goff");
    tFundo->Draw("mH >> hFundo", "mH > 0", "goff");

    if (hSinal->Integral() > 0) hSinal->Scale(1.0 / hSinal->Integral());
    if (hFundo->Integral() > 0) hFundo->Scale(1.0 / hFundo->Integral());

    hSinal->SetLineColor(kBlue + 1);
    hSinal->SetLineWidth(3);
    hSinal->SetFillColorAlpha(kBlue + 1, 0.30);
    hSinal->SetStats(0);
    hSinal->GetYaxis()->SetRangeUser(0, std::max(hSinal->GetMaximum(), hFundo->GetMaximum()) * 1.25);
    hSinal->Draw("HIST");

    hFundo->SetLineColor(kRed + 1);
    hFundo->SetLineWidth(3);
    hFundo->SetFillColorAlpha(kRed + 1, 0.30);
    hFundo->Draw("HIST SAME");

    TLegend *leg = new TLegend(0.60, 0.72, 0.88, 0.88);
    leg->AddEntry(hSinal, "Sinal: H -> b#bar{b}", "f");
    leg->AddEntry(hFundo, "Fundo: QCD b#bar{b}", "f");
    leg->SetBorderSize(0);
    leg->Draw();

    c1->SaveAs("higgs_massa_sobreposto.png");
}
