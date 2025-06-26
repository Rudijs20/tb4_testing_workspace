import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

threshold = [0.23, 0.15, 0.1] # Very forgiving used for Map3
# threshold = 0.15  # Meadien forgivenes used for Map2
# threshold = 0.23  # Strict (no forgivenes) used for Map1

normal_speed_threshold = 0.26  # Speed indicating normal operation

maps = ['Map1', 'Map2', 'Map3']
# maps = ['Map3']
controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/AllResults/'

# Set seaborn style with clean fonts
sns.set_theme(style="whitegrid", context="paper", palette="colorblind")
plt.rcParams["font.family"] = "DejaVu Sans"  # Clean, modern font
plt.rcParams["font.size"] = 12
plt.rcParams["axes.titlesize"] = 14  # Title stays same
plt.rcParams["axes.labelsize"] = 13
plt.rcParams["xtick.labelsize"] = 13
plt.rcParams["ytick.labelsize"] = 13
plt.rcParams["legend.fontsize"] = 12
plt.rcParams["legend.title_fontsize"] = 11

# Custom color palette
palette = {"DWB": "#4C72B0", "MPPI": "#DD8452", "RPP": "#55A868"}

results = []
i = 0

for map_name in maps:
    for ctrl in controllers:
        folder = os.path.join(base_dir, map_name, f"{map_name}_{ctrl}")
        files = glob.glob(os.path.join(folder, 'cmd_vel_log*.csv'))

        for f in files:
            # Read CSV WITH HEADER
            df = pd.read_csv(f)
            
            # Convert necessary columns to numeric
            df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
            df['linear_x'] = pd.to_numeric(df['linear_x'], errors='coerce')
            
            # Trim startup and shutdown phases
            # Find first index where speed reaches normal operation (>= 0.26)
            start_idx = df[df['linear_x'] >= normal_speed_threshold].first_valid_index()
            # Find last index where speed is in normal operation (>= 0.26)
            end_idx = df[df['linear_x'] >= normal_speed_threshold].last_valid_index()
            
            # If valid indices found, trim the dataframe
            if start_idx is not None and end_idx is not None and start_idx < end_idx:
                df = df.loc[start_idx:end_idx].copy()
            else:
                # Skip file if we can't find valid operation window
                print(f"Skipping file {f} - insufficient normal operation data")
                continue
            
            # Calculate time differences
            df['time_diff'] = df['timestamp'].diff().shift(-1)  # Forward difference
            
            # Create stutter mask
    
            stutter_mask = df['linear_x'] < threshold[i]
            
            # Calculate total stutter time
            stutter_time = df.loc[stutter_mask, 'time_diff'].sum(skipna=True)
            
            # If no stutter occurred, stutter_time might be NaN - convert to 0
            stutter_time = stutter_time if not np.isnan(stutter_time) else 0.0
            
            # Count stutter events
            stutter_events = (stutter_mask & ~stutter_mask.shift(fill_value=False)).sum()

            results.append({
                'Map': map_name,
                'Controller': ctrl,
                'File': os.path.basename(f),
                'StutterTime_s': stutter_time,
                'StutterEvents': stutter_events
            })
    i=i+1
            

# Create DataFrame and save CSV
stutter_df = pd.DataFrame(results)
summary = stutter_df.groupby(['Map', 'Controller'])[['StutterTime_s', 'StutterEvents']].mean().reset_index()
summary.to_csv('stutter_summary.csv', index=False)

# Plotting with enhanced styling
fig, axs = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

# Plot Stutter Time
ax1 = sns.barplot(
    data=summary,
    x="Map",
    y="StutterTime_s",
    hue="Controller",
    palette=palette,
    edgecolor=".2",
    linewidth=1.5,
    saturation=0.9,
    ax=axs[0]
)

# Add value labels
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.2f', padding=3, fontsize=10)

# ax1.set_title("Average Stutter Time", fontsize=14, fontweight="bold", pad=15)
ax1.set_ylabel("Stutter Time (s)", labelpad=10)
ax1.set_xlabel("")
ax1.legend().remove()  # Remove individual legends since we'll have one shared
sns.despine(ax=ax1, left=True, bottom=True)

# Plot Stutter Events
ax2 = sns.barplot(
    data=summary,
    x="Map",
    y="StutterEvents",
    hue="Controller",
    palette=palette,
    edgecolor=".2",
    linewidth=1.5,
    saturation=0.9,
    ax=axs[1]
)

# Add value labels
for container in ax2.containers:
    ax2.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

# ax2.set_title("Average Stutter Events", fontsize=14, fontweight="bold", pad=15)
ax2.set_ylabel("Stutter Events", labelpad=10)
ax2.set_xlabel("")
ax2.legend(title="Planner", frameon=True, shadow=True, loc="best")
sns.despine(ax=ax2, left=True, bottom=True)


# Save and show
plt.savefig('stutter_analysis_plots_Map3_Sim.png', dpi=300, bbox_inches='tight')
plt.show()