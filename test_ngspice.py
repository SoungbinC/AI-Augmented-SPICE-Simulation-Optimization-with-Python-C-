from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit("RC Test")
circuit.V(1, "vin", circuit.gnd, 5 @ u_V)
circuit.R(1, "vin", "n1", 1 @ u_kΩ)
circuit.C(1, "n1", circuit.gnd, 1 @ u_uF)

simulator = circuit.simulator()
analysis = simulator.transient(step_time=1e-6, end_time=0.01)

print(f"Simulation ran with {len(analysis.time)} time steps.")
