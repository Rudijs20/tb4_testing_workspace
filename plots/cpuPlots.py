import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os


controllers = ['Map1_DWB', 'Map1_MPPI', 'Map1_RPP']
base_dir = '/home/rudolfs/ros2_ws/AllResults/Map1/'
common_time = np.arange(0, 600, 1)  # Adjust to your log duration

cpu_results = {}

for ctrl in controllers:
    folder = os.path.join(base_dir, ctrl)
    files = sorted(glob.glob(os.path.join(folder, 'nav2_cpu_usage_*.csv')))
    usage_runs = []

    for file in files:
        df = pd.read_csv(file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()
        interp = np.interp(common_time, df['time'], df['controller_server'], left=np.nan, right=np.nan)
        usage_runs.append(interp)

    usage_runs = np.array(usage_runs)
    cpu_results[ctrl] = {
        'mean': np.nanmean(usage_runs, axis=0),
        'std': np.nanstd(usage_runs, axis=0)
    }
# Controller Server CPU % over Time
plt.figure(figsize=(10, 6))
for ctrl, data in cpu_results.items():
    plt.plot(common_time, data['mean'], label=f'{ctrl}')
    plt.fill_between(common_time,
                     data['mean'] - data['std'],
                     data['mean'] + data['std'],
                     alpha=0.2)
plt.title('Controller Server CPU Usage Over Time')
plt.xlabel('Time (s)')
plt.ylabel('CPU Usage (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
