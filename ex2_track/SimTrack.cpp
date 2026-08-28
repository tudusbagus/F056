#include "SimTrack.h"

SimTrack::SimTrack() : Track(), pdgId_(0) {}

SimTrack::SimTrack(double pt, double eta, double phi, int charge, int pdgId)
    : Track(pt, eta, phi, charge), pdgId_(pdgId) {}

SimTrack::~SimTrack() {}

int SimTrack::PdgId() const { return pdgId_; }
