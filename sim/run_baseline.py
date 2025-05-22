from rc_circuit import build_rc_circuit, run_simulation
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("baseline", exist_ok=True)

# Simulate
circuit = build_rc_circuit()
time, v_n1, v_n2 = run_simulation(circuit)

# Save both waveforms
np.save("baseline/time.npy", time)
np.save("baseline/v_n1.npy", v_n1)
np.save("baseline/v_n2.npy", v_n2)

# Plot both
plt.plot(time, v_n1, label="V(n1)")
plt.plot(time, v_n2, label="V(n2)")
plt.title("RC Circuit Baseline Waveforms")
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.legend()
plt.grid(True)
plt.savefig("baseline/waveform.png")
plt.show()
