import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

maps = ['Map1', 'Map2', 'Map3']
controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/AllResults/'

colors = {'DWB': 'blue', 'MPPI': 'red', 'RPP': 'green'}

# Create a figure for each map
for map_name in maps:
    plt.figure(figsize=(12, 8))
    plt.title(f'Controller Server CPU Usage - {map_name}')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 30)  # CPU percentage range
    
    # Track all handles for legend
    legend_handles = []
    
    for ctrl in controllers:
        folder = os.path.join(base_dir, map_name, f"{map_name}_{ctrl}")
        files = glob.glob(os.path.join(folder, 'nav2_cpu_usage*.csv'))
        
        if not files:
            print(f"No CPU usage files found for {map_name} {ctrl}")
            continue
            
        # Process each file
        for f in files:
            df = pd.read_csv(f)
            
            # Convert timestamp to datetime and calculate elapsed time
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            start_time = df['timestamp'].iloc[0]
            df['elapsed_time'] = (df['timestamp'] - start_time).dt.total_seconds()
            
            # Plot controller_server CPU usage
            line, = plt.plot(df['elapsed_time'], df['controller_server'], 
                             color=colors[ctrl], alpha=0.3)
        
        # Create a proxy artist for the legend
        proxy_artist = plt.Line2D([0], [0], color=colors[ctrl], label=ctrl)
        legend_handles.append(proxy_artist)
    
    # Add legend and save figure
    plt.legend(handles=legend_handles)
    plt.tight_layout()
    plt.savefig(f"controller_cpu_usage_{map_name}.png")
    plt.close()

print("Generated CPU usage graphs for all maps")