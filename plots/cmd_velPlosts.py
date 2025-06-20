import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/Map1/'
common_time = np.arange(0, 600, 0.1)  # adjust total time and step

results = {ctrl: {'linear_x': [], 'angular_z': []} for ctrl in controllers}

for ctrl in controllers:
    folder = os.path.join(base_dir, ctrl)
    files = glob.glob(os.path.join(folder, 'cmd_vel_log_*.csv'))

    for file in files:
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        # Assuming timestamp is already sim time in seconds (float)
        interp_linear_x = np.interp(common_time, df['timestamp'], df['linear_x'], left=np.nan, right=np.nan)
        interp_angular_z = np.interp(common_time, df['timestamp'], df['angular_z'], left=np.nan, right=np.nan)

        results[ctrl]['linear_x'].append(interp_linear_x)
        results[ctrl]['angular_z'].append(interp_angular_z)

# Plot linear_x
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
for ctrl in controllers:
    arr = np.array(results[ctrl]['linear_x'])
    mean = np.nanmean(arr, axis=0)
    std = np.nanstd(arr, axis=0)
    plt.plot(common_time, mean, label=ctrl)
    plt.fill_between(common_time, mean - std, mean + std, alpha=0.2)
plt.title('Linear X Velocity over Time')
plt.xlabel('Sim Time (s)')
plt.ylabel('linear_x (m/s)')
plt.legend()
plt.grid(True)

# Plot angular_z
plt.subplot(1, 2, 2)
for ctrl in controllers:
    arr = np.array(results[ctrl]['angular_z'])
    mean = np.nanmean(arr, axis=0)
    std = np.nanstd(arr, axis=0)
    plt.plot(common_time, mean, label=ctrl)
    plt.fill_between(common_time, mean - std, mean + std, alpha=0.2)
plt.title('Angular Z Velocity over Time')
plt.xlabel('Sim Time (s)')
plt.ylabel('angular_z (rad/s)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
