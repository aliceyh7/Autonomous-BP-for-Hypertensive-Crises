import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load simulation data
data = pd.read_csv("simulation_results.csv")
print("Data loaded successfully. Preview:")
print(data.head())

# Define target ranges
TARGET_BP = 90
TARGET_RANGE = (TARGET_BP - 10, TARGET_BP + 10)  # ±10 mmHg
TIGHT_RANGE = (TARGET_BP - 1, TARGET_BP + 1)  # ±1 mmHg

# Generate a complete data table
print("\nGenerating complete data table...")
complete_table = data.pivot(index='Time', columns='Patient', values='BP_Treatment')
complete_table = complete_table.fillna(0)  # Replace NaN values with 0 if any
complete_table.to_csv("complete_bp_table.csv")
print("Complete data table saved as 'complete_bp_table.csv'.")

# Analyze BP metrics
print("\nAnalyzing BP metrics...")
# Calculate median and IQR values for BP at various intervals
bp_stats = data.groupby('Time')['BP_Treatment'].describe(percentiles=[0.25, 0.5, 0.75])
print("BP Stats (Median/IQR at various intervals):")
print(bp_stats)

# Calculate percentage of time outside the target range
data['Outside_Target'] = (data['BP_Treatment'] < TARGET_RANGE[0]) | (data['BP_Treatment'] > TARGET_RANGE[1])
seconds_out_of_range = data.groupby('Patient')['Outside_Target'].sum()
patient_seconds_out_of_range = seconds_out_of_range.sum()

print(f"\nPercentage of patient-seconds outside target range: "
      f"{patient_seconds_out_of_range / (len(data['Time'].unique()) * len(data['Patient'].unique())) * 100:.2f}%")

# Infusion rate changes and medication dose analysis
print("\nAnalyzing infusion rate changes and medication doses...")
infusion_changes = data.groupby('Patient')['Infusion_Rate'].apply(lambda x: (x.diff() != 0).sum())
infusion_summary = infusion_changes.describe()
dose_summary = data.groupby('Patient')['Infusion_Rate'].agg(['mean', 'median', 'max', 'min'])

print("\nInfusion Rate Changes Summary:")
print(infusion_summary)

print("\nMedication Dose Summary (Mean, Median, Max, Min):")
print(dose_summary)

# Visualize results
print("\nGenerating plots...")

# Plot BP for the treatment group
plt.figure(figsize=(12, 6))
for patient in data['Patient'].unique():
    patient_data = data[data['Patient'] == patient]
    plt.plot(patient_data['Time'], patient_data['BP_Treatment'], alpha=0.5)

# Add target range lines
plt.axhline(TARGET_RANGE[0], color="r", linestyle="--", label="Target Lower Bound")
plt.axhline(TARGET_RANGE[1], color="g", linestyle="--", label="Target Upper Bound")
plt.axhline(TARGET_BP, color="b", linestyle="-", label="Target BP")

plt.xlabel("Time (s)")
plt.ylabel("Blood Pressure (mmHg)")
plt.title("Blood Pressure Regulation - Treatment Group")
plt.legend()
plt.savefig("bp_treatment_plot.png", dpi=300)
print("Plot saved as 'bp_treatment_plot.png'.")
plt.show()

# Optionally, analyze alternative PID parameters
print("\nOptional: To analyze alternative PID parameters, modify the PID control parameters and re-run the simulation.")

print("\nAnalysis complete!")
