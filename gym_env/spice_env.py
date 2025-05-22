import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time

from sim.rc_circuit import build_rc_circuit, run_simulation
from sim.waveform_utils import compute_waveform_mse


class SpiceSimEnv(gym.Env):
    def __init__(self, baseline_voltage, alpha=1.0, beta=10.0):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.baseline_voltage = baseline_voltage

        # Action space: log10(timestep) ∈ [log10(1e-7), log10(1e-4)]
        self.action_space = spaces.Box(
            low=np.log10(1e-7), high=np.log10(1e-4), shape=(1,), dtype=np.float32
        )

        # Observation: log timestep
        self.observation_space = spaces.Box(
            low=np.log10(1e-7), high=np.log10(1e-4), shape=(1,), dtype=np.float32
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_timestep = 1e-6
        obs = np.array([np.log10(self.current_timestep)], dtype=np.float32)
        return obs, {}

    def step(self, action):
        log_ts = float(action[0])
        timestep = np.clip(10**log_ts, 1e-7, 1e-4)
        self.current_timestep = timestep

        try:
            circuit = build_rc_circuit()
            start = time.time()
            _, _, v_n2 = run_simulation(circuit, timestep=timestep)  # Use V(n2) only
            runtime = time.time() - start

            mse = compute_waveform_mse(v_n2, self.baseline_voltage)
            reward = -self.alpha * runtime + self.beta * (1 - mse)

            obs = np.array([np.log10(timestep)], dtype=np.float32)
            return obs, reward, True, False, {"runtime": runtime, "mse": mse}

        except Exception as e:
            print(f"[ERROR] Simulation failed: {e}")
            obs = np.array([np.log10(timestep)], dtype=np.float32)
            return obs, -10.0, True, False, {"error": str(e)}

    def render(self, mode="human"):
        print(f"Timestep used: {self.current_timestep:.2e}")
