from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import numpy as np


def build_rc_circuit():
    circuit = Circuit("2-Stage RC Filter")

    # Step input
    circuit.PulseVoltageSource(
        1,
        "vin",
        circuit.gnd,
        initial_value=0 @ u_V,
        pulsed_value=5 @ u_V,
        pulse_width=10 @ u_ms,
        period=20 @ u_ms,
    )

    # First RC stage
    circuit.R(1, "vin", "n1", 1 @ u_kΩ)
    circuit.C(1, "n1", circuit.gnd, 1 @ u_uF)

    # Second RC stage
    circuit.R(2, "n1", "n2", 2 @ u_kΩ)
    circuit.C(2, "n2", circuit.gnd, 0.5 @ u_uF)

    return circuit


def run_simulation(circuit, timestep=1e-6, stop_time=0.01):
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=timestep, end_time=stop_time)

    time = np.array(analysis.time)
    v_n1 = np.array(analysis["n1"])
    v_n2 = np.array(analysis["n2"])
    return time, v_n1, v_n2
