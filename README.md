# Blood Pressure Simulation and Regulation System

This project focuses on simulating and regulating blood pressure using automated control systems, as described in the accompanying manuscript. The study explores the use of a Proportional-Integral-Derivative (PID) control algorithm to regulate blood pressure in hypertensive patients. It models blood pressure dynamics, compares control versus treatment groups, and evaluates the effectiveness of autonomous regulation systems in achieving and maintaining target blood pressure levels.

## Manuscript Overview

The manuscript provides:
- A detailed description of the physiological blood pressure model.
- The rationale for using PID control algorithms to regulate mean arterial pressure (MAP).
- Outcomes from 20,000 simulated cases, split between control (untreated) and intervention (treated with PID control) groups.

For further details on the project, please refer to the manuscript.

## `unified_bp_simulation.py` Overview

The `unified_bp_simulation.py` script is the main implementation of the simulation and regulation system. It models the blood pressure dynamics for a group of patients using both untreated control group simulations and a PID-regulated treatment group. Below is an outline of the key steps in the script:

### Key Steps in `unified_bp_simulation.py`

1. **Simulation Parameters**:
   - Defines the simulation duration (`SIMULATION_TIME`), the number of patients (`NUM_PATIENTS`), and the time step (`TIME_STEP`).
   - Configures PID control parameters (`P`, `I`, `D`) and the target blood pressure range.

2. **Generate BP Profiles**:
   - Uses the `generate_bp_profile()` function to create blood pressure profiles with spikes, dips, and sustained phases, mimicking real-life fluctuations.

3. **Windkessel Model**:
   - Implements a mathematical model of blood pressure dynamics (`windkessel_model`) to simulate the effect of infusion rates on mean arterial pressure (MAP).

4. **Run Simulations**:
   - Simulates the control group with untreated blood pressure.
   - Simulates the treatment group using a PID controller to adjust infusion rates based on deviations from the target MAP.

5. **Data Logging**:
   - Logs time, blood pressure (control and treatment), and infusion rates for each patient across the simulation.

6. **Metrics Calculation**:
   - Evaluates patient-specific metrics, such as the time spent outside the target blood pressure range and the number of infusion rate adjustments.

7. **Results Storage**:
   - Combines results for all patients into a single CSV file (`simulation_results.csv`) for further analysis.

8. **Visualization**:
   - Plots the blood pressure dynamics for the treatment group, showing how the PID controller regulates blood pressure over time.

### How to Run the Script

Run the simulation with:
```bash
python unified_bp_simulation.py
