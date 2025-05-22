import numpy as np
from stable_baselines3 import PPO, A2C, SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
from gym_env.spice_env import SpiceSimEnv
import os

# === Load target waveform: v_n2 (from 2-stage RC circuit) ===
baseline_voltage = np.load("baseline/v_n2.npy")

# === Output directories ===
os.makedirs("logs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# === Algorithms to train ===
agent_configs = {"PPO": PPO, "A2C": A2C, "SAC": SAC}

# === Train each agent ===
for name, AlgoClass in agent_configs.items():
    print(f"\n=== Training {name} ===")

    # Create monitored Gym environment
    env = Monitor(SpiceSimEnv(baseline_voltage))

    # Enable TensorBoard logging
    model = AlgoClass(
        "MlpPolicy",
        env,
        verbose=1,
        tensorboard_log=f"logs/{name}",  # ✅ this enables TB logging
    )

    # Evaluation callback logs mean reward to .npz
    eval_callback = EvalCallback(
        env,
        eval_freq=500,
        log_path=f"logs/{name}",
        best_model_save_path=f"models/{name}",
    )

    # Train
    model.learn(total_timesteps=10000, callback=eval_callback)

    # Save final model
    model.save(f"models/{name}_final")
