import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Base directory where all the Map folders are located
base_dir = '/home/rudolfs/ros2_ws/AllResults'

# Prepare a list to store results
data = []

# Loop through each map (environment)
for env_folder in sorted(os.listdir(base_dir)):
    env_path = os.path.join(base_dir, env_folder)
    if not os.path.isdir(env_path):
        continue

    # Loop through each controller folder inside the environment
    for planner_folder in sorted(os.listdir(env_path)):
        planner_path = os.path.join(env_path, planner_folder)
        if not os.path.isdir(planner_path):
            continue

        # Find all nav2_cpu_usage CSV files
        csv_files = glob.glob(os.path.join(planner_path, 'nav2_cpu_usage_*.csv'))

        for file in csv_files:
            try:
                df = pd.read_csv(file)
                mean_cpu = df['controller_server'].mean()
                data.append({
                    'Environment': env_folder,               # e.g., Map1
                    'Planner': planner_folder.split('_')[-1],  # DWB, MPPI, or RPP
                    'MeanCPU': mean_cpu
                })
            except Exception as e:
                print(f"Error reading {file}: {e}")

# Convert to DataFrame
df_cpu = pd.DataFrame(data)

# Preview the data
print(df_cpu.head())

for env_name in df_cpu['Environment'].unique():
    df_env = df_cpu[df_cpu['Environment'] == env_name]
    
    # Create a 3-panel plot: one for each planner
    g = sns.FacetGrid(df_env, col='Planner', col_wrap=3, height=4, sharex=True, sharey=True)
    g.map_dataframe(sns.histplot, x='MeanCPU', kde=True, bins=15, color='skyblue')
    g.set_titles('{col_name} Planner')
    g.set_axis_labels('Mean CPU Usage (%)', 'Frequency')
    g.fig.suptitle(f'CPU Usage Distribution per Planner in {env_name}', fontsize=16, y=1.05)
    plt.tight_layout()
    plt.show()
