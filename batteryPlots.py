import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
import glob
import os

controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/Map1/'
common_time = np.arange(0, 600, 1)  # Adjust based on max sim time

results = {}

for ctrl in controllers:
    folder = os.path.join(base_dir, ctrl)
    files = sorted(glob.glob(os.path.join(folder, 'battery_log_*.csv')))
    power_runs, energy_runs = [], []

    for file in files:
        df = pd.read_csv(file)
        df['time'] = df['time'] - df['time'].iloc[0]
        df['abs_current'] = abs(df['current'])
        df['power'] = df['voltage'] * df['abs_current']
        df['energy'] = cumulative_trapezoid(df['power'], df['time'], initial=0)

        power_interp = np.interp(common_time, df['time'], df['power'], left=np.nan, right=np.nan)
        energy_interp = np.interp(common_time, df['time'], df['energy'], left=np.nan, right=np.nan)

        power_runs.append(power_interp)
        energy_runs.append(energy_interp)

    results[ctrl] = {
        'power_mean': np.nanmean(power_runs, axis=0),
        'power_std': np.nanstd(power_runs, axis=0),
        'energy_mean': np.nanmean(energy_runs, axis=0),
        'energy_std': np.nanstd(energy_runs, axis=0)
    }

# Cumulative Energy over Time
plt.figure(figsize=(10, 6))
for ctrl, data in results.items():
    plt.plot(common_time, data['energy_mean'], label=f'{ctrl}')
    plt.fill_between(common_time,
                     data['energy_mean'] - data['energy_std'],
                     data['energy_mean'] + data['energy_std'],
                     alpha=0.2)
plt.title('Cumulative Energy Consumption Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Energy (Joules)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Power over Time
plt.figure(figsize=(10, 6))
for ctrl, data in results.items():
    plt.plot(common_time, data['power_mean'], label=f'{ctrl}')
    plt.fill_between(common_time,
                     data['power_mean'] - data['power_std'],
                     data['power_mean'] + data['power_std'],
                     alpha=0.2)
plt.title('Average Power Consumption Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
