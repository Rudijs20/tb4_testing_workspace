import pandas as pd
import os
import glob
from scipy.stats import shapiro, levene

# Folder structure
base_dir = os.path.expanduser("~/ros2_ws/AllResults/")
maps = ['Map1', 'Map2', 'Map3']
controllers = ['DWB', 'MPPI', 'RPP']

# Aggregated data
all_data = []

for map_name in maps:
    for ctrl in controllers:
        folder_name = f"{map_name}_{ctrl}"
        folder_path = os.path.join(base_dir, map_name, folder_name)

        # Battery % used
        battery_files = glob.glob(os.path.join(folder_path, 'battery_log_*.csv'))
        for f in battery_files:
            df = pd.read_csv(f)
            battery_used = df['percentage'].iloc[0] - df['percentage'].iloc[-1]
            all_data.append({
                'Map': map_name,
                'Controller': ctrl,
                'Metric': 'BatteryUsed_%',
                'Value': battery_used
            })

        # CPU usage (controller_server only)
        cpu_files = glob.glob(os.path.join(folder_path, 'nav2_cpu_usage_*.csv'))
        for f in cpu_files:
            df = pd.read_csv(f)
            cpu_mean = df['controller_server'].mean()
            all_data.append({
                'Map': map_name,
                'Controller': ctrl,
                'Metric': 'CPU_Usage',
                'Value': cpu_mean
            })

        # # Execution Time and Path Length
        # metric_files = glob.glob(os.path.join(folder_path, 'navigation_metrics_*.csv'))
        # for f in metric_files:
        #     df = pd.read_csv(f)
        #     for _, row in df.iterrows():
        #         all_data.append({
        #             'Map': map_name,
        #             'Controller': ctrl,
        #             'Metric': 'ExecutionTime_s',
        #             'Value': row['Execution Time (s)']
        #         })
        #         all_data.append({
        #             'Map': map_name,
        #             'Controller': ctrl,
        #             'Metric': 'PathLength_m',
        #             'Value': row['Path Length (m)']
        #         })

# Create DataFrame
df_all = pd.DataFrame(all_data)

# Test assumptions for each metric
results = []

for metric in df_all['Metric'].unique():
    df_metric = df_all[df_all['Metric'] == metric]

    # Normality per group
    normality = []
    for name, group in df_metric.groupby(['Map', 'Controller']):
        if len(group) >= 3:  # Shapiro requires at least 3 samples
            stat, pval = shapiro(group['Value'])
            normality.append({'Map': name[0], 'Controller': name[1], 'Metric': metric, 'Test': 'Shapiro', 'p-value': pval})

    # Homogeneity of variances (Levene’s test across all groups)
    groups = [g['Value'].values for _, g in df_metric.groupby(['Map', 'Controller']) if len(g) >= 2]
    if len(groups) > 1:
        stat, pval = levene(*groups)
        normality.append({'Map': 'All', 'Controller': 'All', 'Metric': metric, 'Test': 'Levene', 'p-value': pval})

    results.extend(normality)

# Save to CSV
result_df = pd.DataFrame(results)
result_df.to_csv('/home/rudolfs/ros2_ws/plots/assumption_tests.csv', index=False)
