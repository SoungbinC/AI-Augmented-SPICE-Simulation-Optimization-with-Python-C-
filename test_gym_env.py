from gym_env.spice_env import SpiceSimEnv
import numpy as np

baseline_voltage = np.load("baseline/voltage.npy")

env = SpiceSimEnv(baseline_voltage)
obs = env.reset()

action = env.action_space.sample()
obs, reward, done, info = env.step(action)

print(
    f"Action: {action}, Reward: {reward}, MSE: {info.get('mse')}, Runtime: {info.get('runtime')}"
)
