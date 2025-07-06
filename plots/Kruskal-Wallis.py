import os
import glob
import pandas as pd
from scipy.stats import kruskal

# Base directory where all environment folders are
base_dir = os.path.expanduser("~/ros2_ws/AllResults/")

battery_data = []

# Walk through each environment folder
for env in sorted(os.listdir(base_dir)):
    env_path = os.path.join(base_dir, env)
    if not os.path.isdir(env_path):
        continue

    # Walk through each planner folder (e.g., Map1_DWB, Map1_MPPI, etc.)
    for planner_folder in sorted(os.listdir(env_path)):
        planner_path = os.path.join(env_path, planner_folder)
        if not os.path.isdir(planner_path):
            continue

        planner_name = planner_folder.split('_')[-1]  # Extract DWB, MPPI, RPP
        csv_files = glob.glob(os.path.join(planner_path, 'battery_log_*.csv'))

        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                if 'percentage' in df.columns and not df.empty:
                    battery_used = df['percentage'].iloc[0] - df['percentage'].iloc[-1]
                    battery_data.append({
                        'Environment': env,
                        'Planner': planner_name,
                        'BatteryUsed': battery_used
                    })
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")

# Convert to DataFrame
df_battery = pd.DataFrame(battery_data)

# Preview
print(df_battery.head())

# Run Kruskal-Wallis test across planners (all environments combined)
mppi = df_battery[df_battery['Planner'] == 'MPPI']['BatteryUsed']
dwb = df_battery[df_battery['Planner'] == 'DWB']['BatteryUsed']
rpp = df_battery[df_battery['Planner'] == 'RPP']['BatteryUsed']

print("\n Kruskal-Wallis Test (All Environments Combined):")
stat, p = kruskal(mppi, dwb, rpp)
print(f"H = {stat:.4f}, p = {p:.4f}")
print("→ Significant difference!" if p < 0.05 else "→ No significant difference.")

# Optionally: Run per environment
print("\n Kruskal-Wallis Test per Environment:")
for env in df_battery['Environment'].unique():
    subset = df_battery[df_battery['Environment'] == env]
    mppi = subset[subset['Planner'] == 'MPPI']['BatteryUsed']
    dwb = subset[subset['Planner'] == 'DWB']['BatteryUsed']
    rpp = subset[subset['Planner'] == 'RPP']['BatteryUsed']

    stat, p = kruskal(mppi, dwb, rpp)
    print(f"{env}: H = {stat:.4f}, p = {p:.4f} → {'Significant' if p < 0.05 else 'Not significant'}")
