import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO, A2C, SAC
from gym_env.spice_env import SpiceSimEnv
from sim.rc_circuit import build_rc_circuit, run_simulation
from scipy.interpolate import interp1d

# === Load baseline ===
baseline_voltage = np.load("baseline/v_n2.npy")
time = np.load("baseline/time.npy")

# === Agent configs ===
agents = {"PPO": PPO, "A2C": A2C, "SAC": SAC}

colors = {"PPO": "blue", "A2C": "green", "SAC": "red"}

# === Plot baseline ===
plt.figure(figsize=(10, 6))
plt.plot(time, baseline_voltage, label="Baseline V(n2)", color="black", linewidth=2)

# === Loop over agents ===
for name, AlgoClass in agents.items():
    try:
        print(f"Evaluating {name}...")
        model = AlgoClass.load(f"models/{name}_final.zip")
        env = SpiceSimEnv(baseline_voltage)
        obs, _ = env.reset()
        action, _ = model.predict(obs, deterministic=True)
        timestep = 10 ** float(action[0])
        print(f"  Selected timestep: {timestep:.2e}")

        # Run sim
        _, _, voltage = run_simulation(build_rc_circuit(), timestep=timestep)

        # Interpolate to baseline time
        agent_time = np.linspace(0, 0.01, len(voltage))
        voltage_interp = interp1d(
            agent_time, voltage, kind="linear", fill_value="extrapolate"
        )(time)

        # Plot
        plt.plot(
            time,
            voltage_interp,
            linestyle="--",
            label=f"{name} Output",
            color=colors[name],
        )

    except Exception as e:
        print(f"[!] Failed to evaluate {name}: {e}")

# === Finalize plot ===
plt.title("Agent vs Baseline — RC Circuit Output (Vn2)")
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("visualize/all_agents_waveform_comparison.png")
plt.show()
