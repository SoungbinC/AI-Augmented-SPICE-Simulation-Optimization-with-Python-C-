import gymnasium as gym
from gymnasium import spaces
import numpy as np
from cpp_blocks import RCFilterBlock


class BlockRLEnv(gym.Env):
    def __init__(self, target_waveform, tstop=0.01, time_step=1e-6):
        super().__init__()

        self.tstop = tstop
        self.time_step = time_step  # ✅ FIXED: avoid conflict with method name
        self.target = target_waveform
        self.block = RCFilterBlock()

        self.action_space = spaces.Box(
            low=np.log10([100, 1e-6]), high=np.log10([10000, 10e-6]), dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(2,), dtype=np.float32
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        return np.zeros(2, dtype=np.float32), {}

    def step(self, action):
        action = np.asarray(action).flatten()
        log_r, log_c = action[0], action[1]

        R = 10**log_r
        C = 10**log_c
        self.block.set_parameters(R, C)

        waveform = np.array(
            self.block.simulate(self.tstop, self.time_step)
        )  # ✅ updated
        mse = np.mean((waveform - self.target) ** 2)
        reward = -mse

        return (
            np.zeros(2, dtype=np.float32),
            reward,
            True,
            False,
            {"R": R, "C": C, "mse": mse},
        )
