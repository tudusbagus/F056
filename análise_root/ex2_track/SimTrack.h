#ifndef SIMTRACK_H
#define SIMTRACK_H

#include "Track.h"

class SimTrack : public Track {
private:
    int pdgId_;

public:
    SimTrack();
    SimTrack(double pt, double eta, double phi, int charge, int pdgId);
    virtual ~SimTrack();

    int PdgId() const;
};

#endif
