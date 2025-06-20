# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import glob


# navigation_metrics = glob.glob("/home/rudijs/tb4_testing_workspace/results/navigation_metrics*.csv")
# df = pd.concat([pd.read_csv(f) for f in navigation_metrics], ignore_index=True)

# sns.boxplot(data=df[['Execution Time (s)', 'Path Length (m)', 
#                      'Local Planner Changes', 'Global Planner Changes']])
# plt.title("Navigation Metrics Across 10 Runs")
# plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import glob

# # Load all CPU CSVs
# cpu_files = glob.glob("/home/rudijs/tb4_testing_workspace/results/nav2_cpu_usage_*.csv")  # adjust this path
# all_runs = []

# for file in cpu_files:
#     df = pd.read_csv(file, parse_dates=['timestamp'])
#     df['total_cpu'] = df.drop(columns=['timestamp']).sum(axis=1)
#     df['time'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()
#     all_runs.append(df[['time', 'total_cpu']])

# # Plot all runs
# plt.figure(figsize=(10, 5))
# for i, run in enumerate(all_runs):
#     plt.plot(run['time'], run['total_cpu'], label=f'Run {i+1}')
    
# plt.title("Total CPU Usage Over Time (All Runs)")
# plt.xlabel("Time (s)")
# plt.ylabel("CPU Usage (%)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()



# import pandas as pd
# import matplotlib.pyplot as plt
# from scipy.integrate import cumulative_trapezoid
# import glob
# import os

# # Find all matching files
# file_pattern = '/home/rudolfs/ros2_ws/Map1/RPP/battery_log_*.csv'
# file_list = sorted(glob.glob(file_pattern))

# # Combine all files
# all_data = []

# for file in file_list:
#     df = pd.read_csv(file)
#     df['time'] = df['time'] - df['time'].iloc[0]  # relative time per file
#     df['filename'] = os.path.basename(file)
#     df['power'] = df['voltage'] * abs(df['current'])
#     df['abs_current'] = abs(df['current'])
#     df['cumulative_energy_j'] = cumulative_trapezoid(df['power'], df['time'], initial=0)
#     all_data.append(df)

# # Concatenate into one DataFrame
# battery_data = pd.concat(all_data, ignore_index=True)

# # Plotting
# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
# fig.suptitle('TurtleBot4 Battery Analysis (All Files)', fontsize=16)

# ax1.plot(battery_data['time'], battery_data['voltage'], 'b-', linewidth=1)
# ax1.set_title('Voltage over Time')
# ax1.set_xlabel('Time (s)')
# ax1.set_ylabel('Voltage (V)')
# ax1.grid(True, alpha=0.3)

# ax2.plot(battery_data['time'], battery_data['abs_current'], 'r-', linewidth=1)
# ax2.set_title('Absolute Current over Time')
# ax2.set_xlabel('Time (s)')
# ax2.set_ylabel('Current (A)')
# ax2.grid(True, alpha=0.3)

# ax3.plot(battery_data['time'], battery_data['power'], 'g-', linewidth=1)
# ax3.set_title('Power Consumption over Time')
# ax3.set_xlabel('Time (s)')
# ax3.set_ylabel('Power (W)')
# ax3.grid(True, alpha=0.3)

# ax4.plot(battery_data['time'], battery_data['cumulative_energy_j'], 'm-', linewidth=1)
# ax4.set_title('Cumulative Energy Consumption')
# ax4.set_xlabel('Time (s)')
# ax4.set_ylabel('Energy (Joules)')
# ax4.grid(True, alpha=0.3)

# total_energy = battery_data['cumulative_energy_j'].iloc[-1]
# fig.text(0.5, 0.01, f'Total Energy Consumed: {total_energy:.2f} Joules', 
#          ha='center', fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5))

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.savefig('battery_analysis_all.png', dpi=300)
# plt.show()

# # Summary
# print(f"\n{' Energy Consumption Summary (All Files) ':-^50}")
# print(f"Total simulation time: {battery_data['time'].iloc[-1]:.2f} seconds")
# print(f"Total energy consumed: {total_energy:.2f} Joules")
# print(f"Average power: {battery_data['power'].mean():.4f} Watts")
# print(f"Min voltage: {battery_data['voltage'].min():.4f} V")
# print(f"Max current: {battery_data['abs_current'].max():.4f} A")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
import glob

file_pattern = '/home/rudolfs/ros2_ws/Map1/RPP/battery_log_*.csv'
file_list = sorted(glob.glob(file_pattern))

# Resample time base: e.g., every 1 second up to max duration
common_time = np.arange(0, 600, 1)  # adjust based on max expected duration

metrics = {
    'voltage': [],
    'current': [],
    'power': [],
    'energy': []
}

for file in file_list:
    df = pd.read_csv(file)
    df['time'] = df['time'] - df['time'].iloc[0]
    df['abs_current'] = abs(df['current'])
    df['power'] = df['voltage'] * df['abs_current']
    df['energy'] = cumulative_trapezoid(df['power'], df['time'], initial=0)

    # Interpolate to common time base
    interp = lambda col: np.interp(common_time, df['time'], df[col], left=np.nan, right=np.nan)

    for key in metrics:
        metrics[key].append(interp(key))

# Convert to numpy arrays
for key in metrics:
    metrics[key] = np.array(metrics[key])

# Compute mean and std
mean = {k: np.nanmean(v, axis=0) for k, v in metrics.items()}
std = {k: np.nanstd(v, axis=0) for k, v in metrics.items()}

plt.figure(figsize=(10, 6))
plt.plot(common_time, mean['power'], label='Mean Power', color='green')
plt.fill_between(common_time, mean['power'] - std['power'], mean['power'] + std['power'],
                 color='green', alpha=0.3, label='±1 Std Dev')
plt.title('Average Power Consumption over Time')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.legend()
plt.grid(True)
plt.show()
