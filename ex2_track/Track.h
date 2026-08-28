#ifndef TRACK_H
#define TRACK_H

class Track {
protected:
    double pt_;
    double eta_;
    double phi_;
    int charge_;

public:
    Track();
    Track(double pt, double eta, double phi, int charge);
    virtual ~Track();

    double Pt() const;
    double Eta() const;
    double Phi() const;
    int Charge() const;

    double Px() const;
    double Py() const;
    double Pz() const;
    double P() const;
};

#endif
