import sys
import os

sys.path.append(os.path.dirname(__file__))

from cpp_blocks import RCFilterBlock


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


st.title("⚙️ RL-Powered Analog Design: RC Filter")

R = st.slider("Resistor R (Ohms)", 100, 10000, 1000)
C = st.slider("Capacitor C (uF)", 1, 10, 1) * 1e-6
tstop = st.slider("Sim Time (ms)", 1, 20, 10) / 1000
step = 1e-6

block = RCFilterBlock()
block.set_parameters(R, C)
waveform = block.simulate(tstop, step)

time = np.linspace(0, tstop, len(waveform))
fig, ax = plt.subplots()
ax.plot(time * 1000, waveform)
ax.set_title("Output Voltage")
st.pyplot(fig)

st.metric("Cutoff Freq", f"{block.get_cutoff():.1f} Hz")

if st.button("🧠 Optimize with RL"):
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_util import make_vec_env
    from rl_env.block_rl_env import BlockRLEnv

    st.write("Training agent...")

    env = make_vec_env(lambda: BlockRLEnv(waveform), n_envs=1)
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=3000)

    # Test agent
    obs = env.reset()
    action, _ = model.predict(obs)

    # Fix: ensure action is unpacked properly
    if isinstance(action, np.ndarray) and action.ndim == 2:
        log_r, log_c = action[0]
    elif isinstance(action, np.ndarray) and action.ndim == 1:
        log_r, log_c = action
    else:
        raise ValueError(f"Unexpected action shape: {action}")

    R_opt, C_opt = 10**log_r, 10**log_c

    st.success(f"Optimized R: {int(R_opt)} Ω, C: {C_opt * 1e6:.2f} µF")
    block.set_parameters(R_opt, C_opt)
    waveform_opt = block.simulate(tstop, step)
    time = np.linspace(0, tstop, len(waveform_opt))

    fig, ax = plt.subplots()
    ax.plot(time * 1000, waveform, label="Original")
    ax.plot(time * 1000, waveform_opt, label="Optimized", linestyle="--")
    ax.legend()
    ax.set_title("RL-Optimized vs Original Output")
    st.pyplot(fig)
