import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

base_dir = os.path.expanduser("~/ros2_ws/AllResults/")
maps = ['Map1', 'Map2', 'Map3']
controllers = ['DWB', 'MPPI', 'RPP']

# Helper to extract controller folder names
def get_ctrl_folder(map_name, ctrl):
    return f"{map_name}_{ctrl}"

# Collect all data in one DataFrame
all_data = []

for map_name in maps:
    for ctrl in controllers:
        folder = os.path.join(base_dir, map_name, get_ctrl_folder(map_name, ctrl))
        
        # Battery
        battery_files = glob.glob(os.path.join(folder, 'battery_log_*.csv'))
        for f in battery_files:
            df = pd.read_csv(f)
            percent_used = df['percentage'].iloc[0] - df['percentage'].iloc[-1]
            all_data.append({'Map': map_name, 'Controller': ctrl, 'Metric': 'BatteryUsed_%', 'Value': percent_used})

        # CPU
        cpu_files = glob.glob(os.path.join(folder, 'nav2_cpu_usage_*.csv'))
        for f in cpu_files:
            df = pd.read_csv(f)
            mean_cpu = df['controller_server'].mean()
            all_data.append({'Map': map_name, 'Controller': ctrl, 'Metric': 'CPU_Usage', 'Value': mean_cpu})

        # Navigation metrics
        nav_files = glob.glob(os.path.join(folder, 'navigation_metrics_*.csv'))
        for f in nav_files:
            df = pd.read_csv(f)
            for idx, row in df.iterrows():
                all_data.append({'Map': map_name, 'Controller': ctrl, 'Metric': 'ExecutionTime_s', 'Value': row['Execution Time (s)']})
                all_data.append({'Map': map_name, 'Controller': ctrl, 'Metric': 'PathLength_m', 'Value': row['Path Length (m)']})

# Convert to DataFrame
df_all = pd.DataFrame(all_data)

# Save raw collected data
df_all.to_csv("combined_metrics_data.csv", index=False)

# ----------- Two-Way ANOVA ------------
def run_anova(metric_name):
    sub_df = df_all[df_all['Metric'] == metric_name]
    model = ols('Value ~ C(Map) + C(Controller) + C(Map):C(Controller)', data=sub_df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

metrics_to_analyze = df_all['Metric'].unique()
for metric in metrics_to_analyze:
    print(f"\n--- ANOVA for {metric} ---")
    anova = run_anova(metric)
    print(anova)
    anova.to_csv(f'anova_{metric}.csv')

# ----------- Optional: Boxplots ----------
import seaborn as sns

for metric in metrics_to_analyze:
    sub_df = df_all[df_all['Metric'] == metric]
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=sub_df, x='Map', y='Value', hue='Controller')
    plt.title(f"{metric} by Map and Controller")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{metric}_boxplot.png")
    plt.close()
