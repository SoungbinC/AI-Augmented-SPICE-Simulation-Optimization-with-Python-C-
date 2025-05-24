// cpp_blocks/rc_filter.cpp
#include <vector>
#include <cmath>

class RCFilterBlock {
public:
    double R = 1000.0; // ohms
    double C = 1e-6;   // farads

    void set_parameters(double r, double c) {
        R = r; C = c;
    }

    std::vector<double> simulate(double tstop, double step) {
        int N = int(tstop / step);
        std::vector<double> out(N);
        double v = 0.0;
        double tau = R * C;
        for (int i = 0; i < N; ++i) {
            double vin = 1.0;
            v += (step / tau) * (vin - v);
            out[i] = v;
        }
        return out;
    }

    double get_cutoff() {
        return 1.0 / (2 * M_PI * R * C);
    }
};
