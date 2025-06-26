import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Load your compiled DataFrame
df = pd.read_csv("/home/rudolfs/ros2_ws/combined_metrics_data.csv")  # Replace with your actual file

# Filter for CPU_Usage only
cpu_df = df[df["Metric"] == "CPU_Usage"]

# Combine Map and Controller into a single group label (optional but useful)
cpu_df["Group"] = cpu_df["Map"] + "_" + cpu_df["Controller"]

# Run Tukey's HSD
tukey = pairwise_tukeyhsd(endog=cpu_df["Value"], groups=cpu_df["Group"], alpha=0.05)

# Print or save results
print(tukey.summary())


# Optional: plot it
fig = tukey.plot_simultaneous(figsize=(10, 6))
plt.title("Tukey HSD: CPU Usage across Map+Controller groups")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("tukey_cpu_usage.png")
plt.show()
