# AI-Augmented SPICE Simulation Optimization (Python + C++)

## 🎯 Project Summary

This project explores the use of reinforcement learning (PPO, A2C, SAC) to auto-tune SPICE simulation parameters for analog circuits, minimizing runtime without sacrificing waveform accuracy. Inspired by Cadence Cerebrus and the AI inflection point in chip design, it models how RL agents can optimize verification at the circuit level — directly reducing one of the most time-consuming steps in analog/mixed-signal IC design. The project demonstrates that with AI-guided simulation tuning, it's possible to achieve faster, smarter design closure — a key pillar of next-gen AI-powered EDA tools.

---

## 🧩 Key Features

-   🧪 SPICE-based RC circuit simulation using PySpice
-   🧠 PPO agent (via `stable-baselines3`) that tunes timestep dynamically
-   🎯 Custom reward function balancing runtime and waveform similarity
-   🧰 C++-wrapped mock simulation core (via PyBind11)
-   📈 Visualizations for waveform overlay, reward trends, and runtime
-   🧼 Gym-compatible environment with error handling and configurable parameters

---

## 🏗️ Project Structure

spice-rl-optimizer/
│
├── cpp_sim/ # C++ module & PyBind11 wrapper
│ ├── simulation.cpp
│ ├── simulation.h
│ └── bindings.cpp
│
├── gym_env/ # Gym environment
│ └── spice_env.py
│
├── sim/ # SPICE netlists and waveform utilities
│ ├── rc_circuit.py
│ └── waveform_utils.py
│
├── train/ # Training logic & agent configs
│ └── train_rl.py
│
├── visualize/ # Plotting results
│ └── plot_waveforms.py
│
├── notebooks/ # Jupyter playgrounds (optional)
│ └── debug_analysis.ipynb
│
├── baseline/ # Baseline waveforms and logs
│ └── baseline_output.json
│
├── README.md
└── requirements.txt

---

## ⚙️ Workflow Overview

1. **Simulate Baseline**

    - Run RC circuit simulation via PySpice
    - Store baseline waveform and runtime

2. **Build Gym Environment**

    - Action: timestep (and optionally tolerance)
    - Observation: waveform summary or metadata
    - Reward: `-α * runtime + β * (1 - waveform MSE to baseline)`

3. **Train PPO Agent**

    - Use `stable-baselines3` for RL optimization
    - Track waveform error and runtime over episodes

4. **Integrate C++ Simulation**

    - Create a mock C++ simulation core with runtime/waveform output
    - Wrap using PyBind11 to simulate real-world toolchain integration

5. **Visualize Results**
    - Plot waveform overlays (baseline vs RL-optimized)
    - Show runtime improvements and reward progression

---

## 🧠 AI in EDA Context

Cadence’s Q1 2025 milestone — where over 50% of <28nm tapeouts were AI-assisted — signals a transformative shift in chip design. This project reflects the same principles in a focused domain: applying RL to reduce analog simulation costs, avoid unstable configurations, and speed iteration.

Just as Cadence Cerebrus automates RTL-to-GDSII flows, this prototype explores how AI can intelligently assist in simulation-level design loops — enabling faster and safer chip development.

---

## 🔧 Technologies Used

| Component       | Technology             |
| --------------- | ---------------------- |
| Simulation      | PySpice, Ngspice       |
| RL Framework    | stable-baselines3, Gym |
| C++ Integration | PyBind11               |
| Plotting        | Matplotlib             |
| Logging         | JSON, CSV              |
| Development     | Python 3.10+, C++17    |

---

## 🛠 Installation

```bash
# Python dependencies
pip install -r requirements.txt

# PySpice install (Ngspice must be installed separately)
pip install PySpice

# Build C++ module
cd cpp_sim
mkdir build && cd build
cmake ..
make
```
