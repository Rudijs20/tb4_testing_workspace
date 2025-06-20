import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/Map1/'

metrics = {
    'Execution Time (s)': [],
    'Path Length (m)': [],
    'Local Planner Changes': [],
    'Global Planner Changes': []
}

for ctrl in controllers:
    folder = os.path.join(base_dir, ctrl)
    files = glob.glob(os.path.join(folder, 'navigation_metrics*.csv'))
    df_all = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    for key in metrics:
        metrics[key].append(df_all[key].values)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axs = axs.flatten()
for i, (metric, values) in enumerate(metrics.items()):
    axs[i].boxplot(values, labels=controllers)
    axs[i].set_title(metric)
    axs[i].grid(True, alpha=0.3)

plt.suptitle("Navigation Metrics Comparison")
plt.tight_layout()
plt.show()
