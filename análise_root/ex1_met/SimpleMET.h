#ifndef SIMPLEMET_H
#define SIMPLEMET_H

class SimpleMET {
private:
	double mex_;
	double mey_;

public: 
	SimpleMET();
	SimpleMET(double ex, double ey);
	~SimpleMET();

	void Add(double px, double py);

	double Value() const;
	double Ex() const;
	double Ey() const;
	double Phi() const;
};

#endif
