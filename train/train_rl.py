import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from gym_env.spice_env import SpiceSimEnv

# Load baseline waveform
baseline_voltage = np.load("baseline/voltage.npy")

# Create environment
env = SpiceSimEnv(baseline_voltage)

# (Optional) Check if the environment is Gym-compliant
check_env(env, warn=True)

# Instantiate PPO agent
model = PPO("MlpPolicy", env, verbose=1)

# Train for N timesteps
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_spice_timestep")
