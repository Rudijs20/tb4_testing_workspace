import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# Use a professional style
plt.style.use('seaborn-v0_8-colorblind')

maps = ['Map1', 'Map2', 'Map3']
controllers = ['DWB', 'MPPI', 'RPP']
base_dir = '/home/rudolfs/ros2_ws/AllResults/'

# Initialize data collection structures
metrics = {
    'Execution Time (s)': {},
    'Path Length (m)': {},
    'Local Planner Changes': {}
}

# Create a list to store all raw data for CSV export (only successful runs)
all_data = []

# Enhanced debug function
def debug_print(message, level=1):
    indent = "  " * level
    print(f"{indent}{message}")

# Collect data with improved error handling
debug_print("Starting data collection...")
data_found = False

# First pass: Process only successful runs for statistics
for map_name in maps:
    for ctrl in controllers:
        folder = os.path.join(base_dir, map_name, f"{map_name}_{ctrl}")
        debug_print(f"Processing: {folder}", level=1)
        
        # Check if directory exists
        if not os.path.exists(folder):
            debug_print(f"Directory not found! Skipping.", level=2)
            continue
            
        # Search for CSV files in main directory (successful runs)
        pattern = os.path.join(folder, 'navigation_metrics*.csv')
        debug_print(f"Search pattern: {pattern}", level=2)
        files = glob.glob(pattern)
        
        if not files:
            debug_print("No matching files found!", level=2)
            continue
            
        debug_print(f"Found {len(files)} successful runs:", level=2)
        for f in files:
            debug_print(os.path.basename(f), level=3)
            
        # Process each file (successful runs only)
        for f in files:
            try:
                df = pd.read_csv(f)
                # Add map and controller information
                df['Map'] = map_name
                df['Controller'] = ctrl
                df['File'] = os.path.basename(f)
                df['Run_Status'] = 'success'  # Mark as successful run
                all_data.append(df)
                data_found = True
            except Exception as e:
                debug_print(f"Error processing {os.path.basename(f)}: {str(e)}", level=3)
                continue
            
        # Combine files for this map/controller
        try:
            df_all = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
            label = f"{map_name}_{ctrl}"
            
            # Store data for plotting (successful runs only for stats)
            for key in metrics:
                if key in df_all.columns:
                    metrics[key][label] = df_all[key].values
        except Exception as e:
            debug_print(f"Error combining files: {str(e)}", level=3)
            continue

# Second pass: Add failed runs ONLY for visualization (not for stats)
for map_name in maps:
    for ctrl in controllers:
        # Only add failed runs for MPPI on Map3 as per request
        if map_name == 'Map3' and ctrl == 'MPPI':
            failed_folder = os.path.join(base_dir, map_name, f"{map_name}_{ctrl}", 'failed_runs')
            debug_print(f"Processing failed runs: {failed_folder}", level=1)
            
            if not os.path.exists(failed_folder):
                debug_print(f"Failed runs directory not found! Skipping.", level=2)
                continue
                
            # Search for CSV files in failed_runs directory
            pattern = os.path.join(failed_folder, 'navigation_metrics*.csv')
            debug_print(f"Search pattern: {pattern}", level=2)
            failed_files = glob.glob(pattern)
            
            if not failed_files:
                debug_print("No failed run files found!", level=2)
                continue
                
            debug_print(f"Found {len(failed_files)} failed runs:", level=2)
            for f in failed_files:
                debug_print(os.path.basename(f), level=3)
                
            # Process failed runs - ONLY for visualization, not for stats
            try:
                # Combine all failed runs
                df_failed = pd.concat([pd.read_csv(f) for f in failed_files], ignore_index=True)
                label = f"{map_name}_{ctrl}"
                
                # Append failed runs to the existing data for visualization
                for key in metrics:
                    if key in df_failed.columns and label in metrics[key]:
                        # Append failed runs to successful runs for visualization only
                        metrics[key][label] = np.append(metrics[key][label], df_failed[key].values)
            except Exception as e:
                debug_print(f"Error processing failed runs: {str(e)}", level=3)

# Combine all raw data into a single DataFrame for CSV export (only successful runs)
if all_data:
    debug_print("Combining data and generating outputs...")
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Reorder columns
    cols = ['Map', 'Controller', 'Run_Status', 'File'] + [col for col in combined_df.columns if col not in ['Map', 'Controller', 'Run_Status', 'File']]
    combined_df = combined_df[cols]
    
    # Save to CSV
    combined_df.to_csv("nav_metrics_all_data.csv", index=False)
    debug_print("Saved raw data to: nav_metrics_all_data.csv")
    
    # Create summary statistics (only successful runs)
    summary_df = combined_df.groupby(['Map', 'Controller']).agg({
        'Execution Time (s)': ['mean', 'std'],
        'Path Length (m)': ['mean', 'std'],
        'Local Planner Changes': ['mean', 'std']
    }).reset_index()
    
    # Flatten multi-level column index
    summary_df.columns = [' '.join(col).strip() for col in summary_df.columns.values]
    summary_df.to_csv("nav_metrics_summary.csv", index=False)
    debug_print("Saved summary to: nav_metrics_summary.csv")
    
    # Plotting with enhanced aesthetics (including failed runs as outliers)
    debug_print("Generating visualizations...")
    fig, axs = plt.subplots(1, 3, figsize=(20, 8), dpi=100)
    
    # Define a consistent color palette
    controller_colors = {
        'DWB': '#1f77b4',    # Blue
        'MPPI': '#ff7f0e',   # Orange
        'RPP': '#2ca02c'     # Green
    }
    
    # Create consistent positions for each map-controller combination
    positions = {}
    map_spacing = 0.8
    controller_spacing = 0.2
    for map_idx, map_name in enumerate(maps):
        for ctrl_idx, ctrl in enumerate(controllers):
            positions[f"{map_name}_{ctrl}"] = (
                map_idx * map_spacing + ctrl_idx * controller_spacing
            )
    
    # Create custom legend elements
    # from matplotlib.patches import Patch
    # legend_elements = [
    #     Patch(facecolor=controller_colors['DWB'], label='DWB'),
    #     Patch(facecolor=controller_colors['MPPI'], label='MPPI'),
    #     Patch(facecolor=controller_colors['RPP'], label='RPP')
    # ]
    
    # Plot each metric
    for i, (metric, values_dict) in enumerate(metrics.items()):
        # Prepare data and labels
        labels = list(values_dict.keys())
        data = list(values_dict.values())
        
        # Skip if no data
        if not data or not any(len(d) > 0 for d in data):
            debug_print(f"No data available for {metric}, skipping plot", level=2)
            continue
            
        # Create boxplot
        boxprops = dict(linewidth=2, facecolor='white')
        medianprops = dict(linewidth=2.5, color='darkred')
        # Changed to use normal circles instead of red X's
        flierprops = dict(marker='o', markersize=4, markerfacecolor='none', markeredgecolor='black', alpha=0.8)
        
        bp = axs[i].boxplot(
            data, 
            positions=[positions[label] for label in labels],
            widths=0.15,
            patch_artist=True,
            boxprops=boxprops,
            medianprops=medianprops,
            flierprops=flierprops,
            showmeans=False
        )
        
        # Add color to boxes based on controller
        for j, box in enumerate(bp['boxes']):
            ctrl = labels[j].split('_')[1]
            box.set_facecolor(controller_colors[ctrl])
            box.set_alpha(0.8)
        
        # Add grid and set titles
        axs[i].grid(True, linestyle='--', alpha=0.7)
        axs[i].set_title(metric, fontsize=14, fontweight='bold', pad=15)
        axs[i].set_ylabel(metric, fontsize=12, labelpad=10)
        
        # Set x-axis labels and ticks
        axs[i].set_xticks([map_idx * map_spacing + controller_spacing for map_idx in range(len(maps))])
        axs[i].set_xticklabels(maps, fontsize=12)
        axs[i].set_xlabel('Map', fontsize=12, labelpad=10)
        
        # Add minor grid
        axs[i].grid(True, which='minor', linestyle=':', alpha=0.4)
        axs[i].minorticks_on()
        
        # Add light border around each subplot
        for spine in axs[i].spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('#cccccc')
            spine.set_linewidth(1.5)

    # Add figure title and legend
    # fig.suptitle("Navigation Performance Metrics", 
    #             fontsize=18, 
    #             fontweight='bold', 
    #             y=0.98)
    
    # # Add special legend entry for failed runs (updated to circle)
    # from matplotlib.lines import Line2D
    # legend_elements.append(Line2D([0], [0], 
    #                              marker='o', 
    #                              color='w', 
    #                              markerfacecolor='none', 
    #                              markeredgecolor='black',
    #                              markersize=10, 
    #                              label='Failed Runs (Map3 MPPI)'))
    
    # fig.legend(
    #     handles=legend_elements, 
    #     loc='upper center', 
    #     bbox_to_anchor=(0.5, 0.05), 
    #     ncol=4, 
    #     frameon=True,
    #     framealpha=0.9,
    #     fontsize=12,
    #     title='Legend',
    #     title_fontsize=13
    # )
    
    # Adjust spacing
    plt.subplots_adjust(top=0.9, bottom=0.2, wspace=0.25)  # Increased bottom margin
    
    # Add explanatory caption (updated text)
    fig.text(
        0.5, 0.01, 
        "Note: Boxes show quartiles (successful runs only), line shows median. Black circles indicate failed runs.",
        ha='center', 
        fontsize=11, 
        color='#555555'
    )
    
    # Add light background to figure
    fig.set_facecolor('#f5f5f5')
    
    # Save and show
    plt.savefig("nav_metrics_all_maps.png", bbox_inches='tight', dpi=150, facecolor=fig.get_facecolor())
    debug_print("Saved visualization to: nav_metrics_all_maps.png")
    plt.show()
    
else:
    print("\n*** NO DATA FOUND! ***")
    print("Possible solutions:")
    print("1. Check base directory: " + base_dir)
    print("2. Verify directory structure: base_dir/MapX/MapX_Controller/")
    print("3. Confirm file naming pattern: 'navigation_metrics*.csv'")
    print("4. Ensure files exist in controller directories")
    print("5. Check file permissions")