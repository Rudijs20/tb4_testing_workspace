import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = '/home/rudolfs/ros2_ws/AllResults'
maps = ['Map1', 'Map2', 'Map3']
# maps = ['Map1_IRL']
planners = ['DWB', 'MPPI', 'RPP']

results = []

for map_name in maps:
    map_path = os.path.join(base_dir, map_name)
    for planner_name in planners:
        planner_folder = f"{map_name}_{planner_name}"
        planner_path = os.path.join(map_path, planner_folder)

        battery_means = []
        cpu_means = []

        for filename in os.listdir(planner_path):
            if filename.startswith("battery_log"):
                run_id = filename.split("_")[-1].split(".")[0]
                battery_df = pd.read_csv(os.path.join(planner_path, filename))
                battery_means.append(battery_df["percentage"].iloc[0] - battery_df["percentage"].iloc[-1])

            if filename.startswith("nav2_cpu_usage") and "controller_server" in open(os.path.join(planner_path, filename)).readline():
                cpu_df = pd.read_csv(os.path.join(planner_path, filename))
                cpu_means.append(cpu_df["controller_server"].mean())

        # Aggregate
        battery_avg = sum(battery_means) / len(battery_means) if battery_means else None
        battery_avg = battery_avg*100
        cpu_avg = sum(cpu_means) / len(cpu_means) if cpu_means else None

        for b, c in zip(battery_means, cpu_means):
            results.append({
                "Map": map_name,
                "Planner": planner_name,
                "BatteryUsed": b * 100,
                "CPUUsed": c
            })

# Convert to DataFrame
df_raw = pd.DataFrame(results)

df = df_raw.groupby(["Map", "Planner"]).agg(
    BatteryUsageMean=("BatteryUsed", "mean"),
    BatteryUsageStd=("BatteryUsed", "std"),
    CPUUsageMean=("CPUUsed", "mean"),
    CPUUsageStd=("CPUUsed", "std")
).reset_index()

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

# ----- BATTERY USAGE PLOT -----
plt.figure(figsize=(8, 5))
ax = sns.boxplot(
    data=df_raw,
    x="Map",
    y="BatteryUsed",
    hue="Planner",
    palette=palette,
    linewidth=1.5,
    fliersize=3
)

# Add value labels (optional, boxplots usually omit this)
# for container in ax.containers:
#     ax.bar_label(container, fmt='%.2f%%', padding=3, fontsize=10)

plt.ylabel("Battery Percentage Used (%)", labelpad=10)
plt.xlabel("")
plt.ylim(0, df_raw["BatteryUsed"].max() * 1.2)
plt.legend(
    title="Planner",
    loc='upper center',
    ncol=3,
    frameon=True,
    fancybox=True,
    framealpha=0.95,
    facecolor='white',
    edgecolor='gray',
    fontsize=10,
    title_fontsize=11
)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("battery_usage_boxplot.png", dpi=300)
plt.close()


# ----- CPU USAGE PLOT -----
plt.figure(figsize=(8, 5))
ax = sns.boxplot(
    data=df_raw,
    x="Map",
    y="CPUUsed",
    hue="Planner",
    palette=palette,
    linewidth=1.5,
    fliersize=3
)

plt.ylabel("CPU Usage (%)", labelpad=10)
plt.xlabel("")
plt.ylim(0, df_raw["CPUUsed"].max() * 1.3)
plt.legend(
    title="Planner",
    loc='upper center',
    ncol=3,
    frameon=True,
    fancybox=True,
    framealpha=0.95,
    facecolor='white',
    edgecolor='gray',
    fontsize=10,
    title_fontsize=11
)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("cpu_usage_boxplot.png", dpi=300)
plt.close()


