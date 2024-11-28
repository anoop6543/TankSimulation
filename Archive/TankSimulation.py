import numpy as np
import matplotlib.pyplot as plt

# Parameters for the tanks
tank1_max = 100  # Maximum level of tank 1
level1 = 0       # Current level of tank 1

tank2_max = 100  # Maximum level of tank 2
level2 = 0       # Current level of tank 2

# Time settings
time_step = 0.1  # Time step in seconds
sim_time = 300   # Total simulation time in seconds

times = np.arange(0, sim_time, time_step)

# Data recording for visualization
levels1 = []
levels2 = []

# Simulation loop
for t in times:
    # Control Logic for Tank 1
    if level1 < 30:
        control1 = 1  # Start filling at full rate
    elif level1 >= 30 and level1 < 80:
        control1 = 1  # Continue filling at full rate
    elif level1 >= 80 and level1 < 90:
        control1 = 0.5  # Slow down rate
    elif level1 >= 90:
        control1 = 0.25  # Slow down again
    else:
        control1 = 0  # Stop filling

    level1 += control1 * time_step
    level1 = min(level1, tank1_max)  

    # Control Logic for Tank 2
    if level2 < 20:
        control2 = 1  
    elif level2 >= 20 and level2 < 80:
        control2 = 1  
    elif level2 >= 80 and level2 < 90:
        control2 = 0.5  
    elif level2 >= 90:
        control2 = 0.25  
    else:
        control2 = 0  

    level2 += control2 * time_step
    level2 = min(level2, tank2_max)  

    # Record levels for visualization
    levels1.append(level1)
    levels2.append(level2)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(times, levels1, label='Tank 1 Level (%)')
plt.plot(times, levels2, label='Tank 2 Level (%)')
plt.axhline(30, color='blue', linestyle='--', label='Tank 1 Start Filling')
plt.axhline(20, color='orange', linestyle='--', label='Tank 2 Start Filling')
plt.axhline(80, color='green', linestyle='--', label='Slow Down Rate')
plt.axhline(90, color='red', linestyle='--', label='Further Slow Down')
plt.axhline(95, color='purple', linestyle='--', label='Max Level')
plt.xlabel('Time (s)')
plt.ylabel('Level (%)')
plt.title('Two Tank System Simulation')
plt.legend()
plt.grid(True)
plt.show()

