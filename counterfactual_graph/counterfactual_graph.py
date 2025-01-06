"""
Generating the counterfactual graph for SAEM
May 10, 2023.
"""
import random
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import math as m
from cmath import pi
from math import floor

##################################

from matplotlib.pyplot import cm
color = iter(cm.rainbow(np.linspace(0, 1, 1000)))

plt.ion()
fig1, ax1 = plt.subplots(1, 1, num=1, clear=True)
targetMAP = 90

def NoiseMachine(bp, magnitude, endGoal):
    randWeight = np.random.uniform(-0.8, 1.0)
    return bp + (endGoal - bp) * randWeight * magnitude

for i in np.arange(80, 130, 0.05):
    bp = [i]
    trendTo = 150
    magnitude = 0.01
    for timeStep in np.arange(1, 1000, 1):
        bp.append(NoiseMachine(bp[-1], magnitude, trendTo))
        
    xBP = np.arange(1, len(bp)+1)
    
    rainbowColor = next(color)
    ax1.plot(xBP, bp, color=rainbowColor, linewidth=0.5, label=f"Initial BP {i:.1f}")
    
ax1.set(title="Array of 10,000 Patients' BP Without Infusion",
        xlabel="Time (s)", 
        ylabel="Mean Arterial Blood Pressure (mmHg)")
ax1.legend(loc='best')

# Save the plot to the current directory
plt.savefig("blood_pressure_simulation.png", dpi=300)

# Show the plot
plt.show()
