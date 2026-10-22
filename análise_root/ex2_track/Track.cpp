#include "Track.h"
#include <cmath>

Track::Track() : pt_(0.0), eta_(0.0), phi_(0.0), charge_(0) {}

Track::Track(double pt, double eta, double phi, int charge)
    : pt_(pt), eta_(eta), phi_(phi), charge_(charge) {}

Track::~Track() {}

double Track::Pt() const { return pt_; }
double Track::Eta() const { return eta_; }
double Track::Phi() const { return phi_; }
int Track::Charge() const { return charge_; }

double Track::Px() const { return pt_ * std::cos(phi_); }
double Track::Py() const { return pt_ * std::sin(phi_); }
double Track::Pz() const { return pt_ * std::sinh(eta_); }
double Track::P() const { return pt_ * std::cosh(eta_); }

