import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simple_pid import PID
import random

# Simulation Parameters
SIMULATION_TIME = 11000  # seconds
NUM_PATIENTS = 20  # Example patient count
TIME_STEP = 1  # seconds

# PID Parameters (from manuscript assumptions)
P, I, D = 0.75, 0.014, 0.0
TARGET_BP = 90
TARGET_RANGE = (TARGET_BP - 10, TARGET_BP + 10)  # ±10 mmHg
TIGHT_RANGE = (TARGET_BP - 1, TARGET_BP + 1)  # ±1 mmHg

# Windkessel model parameters (from provided files)
b0, bm, a1 = 0.18661, 0.07464, 0.74082
m, d = 3, 3

# Initialize results storage
results = []
out_of_range_seconds = []
infusion_changes = []

# Function to generate BP profiles with spikes, dips, and sustained phases (from EquilTesting_v2.py)
def generate_bp_profile():
    profile = []
    for _ in range(20):
        profile.extend([random.uniform(-2, 2) for _ in range(300)])  # Sustained
        profile.extend([random.uniform(2, 5) for _ in range(100)])  # Spike
        profile.extend([random.uniform(-5, -2) for _ in range(100)])  # Dip
    return profile

# Function to simulate BP response (from new_pid_sim.py and pid_model.py)
def windkessel_model(bp, infusion_rate, previous_map_change):
    map_change = (
        b0 * infusion_rate[d - 1]
        + bm * infusion_rate[d - 1 - m]
        + a1 * previous_map_change
    )
    noise = random.uniform(-2, 2)  # Adding random noise
    new_bp = bp - map_change + noise
    return max(new_bp, 0), map_change  # MAP cannot be negative

# Run simulations
for patient in range(NUM_PATIENTS):
    # Generate identical BP profile for control and treatment
    bp_profile = generate_bp_profile()

    # Initialize variables
    bp = random.uniform(115, 140)  # Starting BP for control and treatment
    infusion_rate = [0] * 100
    previous_map_change = 0
    pid = PID(P, I, D, setpoint=TARGET_BP)
    pid.output_limits = (0, 180)  # Infusion rate limits in ml/hr

    patient_data = {
        "Time": [],
        "BP_Control": [],
        "BP_Treatment": [],
        "Infusion_Rate": []
    }

    control_bp = bp  # Control group BP
    treatment_bp = bp  # Treatment group BP
    infusion_changes_patient = 0

    for t in range(SIMULATION_TIME):
        # Control Group (untreated BP dynamics from untitled0.py)
        control_bp += bp_profile[t % len(bp_profile)]

        # Treatment Group
        error = treatment_bp - TARGET_BP
        infusion = pid(error)
        infusion_rate.append(infusion)
        infusion_rate.pop(0)
        treatment_bp, previous_map_change = windkessel_model(treatment_bp, infusion_rate, previous_map_change)

        if t > 0 and infusion_rate[-1] != infusion_rate[-2]:
            infusion_changes_patient += 1

        # Log data
        patient_data["Time"].append(t)
        patient_data["BP_Control"].append(control_bp)
        patient_data["BP_Treatment"].append(treatment_bp)
        patient_data["Infusion_Rate"].append(infusion)

    # Analyze patient-specific metrics
    bp_within_range = [
        TARGET_RANGE[0] <= bp <= TARGET_RANGE[1]
        for bp in patient_data["BP_Treatment"]
    ]
    seconds_out_of_range = SIMULATION_TIME - sum(bp_within_range)

    results.append(pd.DataFrame(patient_data))
    out_of_range_seconds.append(seconds_out_of_range)
    infusion_changes.append(infusion_changes_patient)

# Combine results into a single DataFrame
all_data = pd.concat(results, keys=range(NUM_PATIENTS))
all_data.to_csv("simulation_results.csv", index=False)

# Summary Metrics
print("Summary:")
print(f"Median infusion changes per patient: {np.median(infusion_changes)}")
print(f"Median seconds out of range per patient: {np.median(out_of_range_seconds)}")

# Visualization
plt.figure(figsize=(10, 6))
for patient_data in results:
    plt.plot(patient_data["Time"], patient_data["BP_Treatment"], alpha=0.5)
plt.axhline(TARGET_RANGE[0], color="r", linestyle="--", label="Target Lower Bound")
plt.axhline(TARGET_RANGE[1], color="g", linestyle="--", label="Target Upper Bound")
plt.xlabel("Time (s)")
plt.ylabel("Blood Pressure (mmHg)")
plt.title("BP Regulation Over Time (Treatment Group)")
plt.legend()
plt.show()
