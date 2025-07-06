import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = os.path.expanduser("~/ros2_ws/AllResults/")
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

        results.append({
            "Map": map_name,
            "Planner": planner_name,
            "BatteryUsageMean": battery_avg,
            "CPUUsageMean": cpu_avg
        })

# Convert to DataFrame
df = pd.DataFrame(results)
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
ax = sns.barplot(
    data=df,
    x="Map",
    y="BatteryUsageMean",
    hue="Planner",
    palette=palette,
    edgecolor=".2",
    linewidth=1.5,
    saturation=0.9
)

# Add value labels
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f%%', padding=3, fontsize=10)

# Styling enhancements
# plt.title("Battery Consumption by Navigation Planner", pad=20, fontweight="bold")
plt.ylabel("Battery Percentage Used (%)", labelpad=10)
plt.xlabel("")
plt.ylim(0, df["BatteryUsageMean"].max() * 1.2)  # Add headroom for labels
plt.legend(
    title="Planner",
    frameon=True,
    shadow=True,
    loc='upper center',  # Positions at top center
    # bbox_to_anchor=(0.5, 1.15),  # Adjust these values to fine-tune position
    ncol=3,  # This creates the horizontal/elongated layout
    fancybox=True,  # Gives rounded corners
    framealpha=0.95,  # Slight transparency
    facecolor='white',  # Background color
    edgecolor='gray',  # Border color
    fontsize=10,
    title_fontsize=11
)

# Remove spines for cleaner look
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("battery_usage_plot.png", dpi=300)
plt.close()

# ----- CPU USAGE PLOT -----
plt.figure(figsize=(8, 5))
ax = sns.barplot(
    data=df,
    x="Map",
    y="CPUUsageMean",
    hue="Planner",
    palette=palette,
    edgecolor=".2",
    linewidth=1.5,
    saturation=0.9
)

# Add value labels
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f%%', padding=3, fontsize=10)

# Styling enhancements
# plt.title("Average CPU Utilization (Controller Server) by Navigation Planner", 
#           pad=20, fontweight="bold")
plt.ylabel("CPU Usage (%)", labelpad=10)
plt.xlabel("")
plt.ylim(0, df["CPUUsageMean"].max() * 1.3)  # Add headroom for labels
plt.legend(
    title="Planner",
    frameon=True,
    shadow=True,
    loc='upper center',  # Positions at top center
    # bbox_to_anchor=(0.5, 1.15),  # Adjust these values to fine-tune position
    ncol=3,  # This creates the horizontal/elongated layout
    fancybox=True,  # Gives rounded corners
    framealpha=0.95,  # Slight transparency
    facecolor='white',  # Background color
    edgecolor='gray',  # Border color
    fontsize=10,
    title_fontsize=11
)

# Add light grid
# ax.yaxis.grid(True, linestyle='--', alpha=0.4)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("cpu_usage_plot.png", dpi=300)
plt.close()
