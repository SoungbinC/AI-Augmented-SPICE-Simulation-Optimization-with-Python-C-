import numpy as np


def compute_waveform_mse(sim_voltage, baseline_voltage):
    min_len = min(len(sim_voltage), len(baseline_voltage))
    v1 = np.array(sim_voltage[:min_len])
    v2 = np.array(baseline_voltage[:min_len])
    return np.mean((v1 - v2) ** 2)
