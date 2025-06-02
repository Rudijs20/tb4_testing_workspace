#!/usr/bin/env python3

import psutil
import time
import csv
from datetime import datetime
import os
import signal
import sys

# Nav2 process names to track
NAV2_PROCESSES = [
    "bt_navigator",
    "planner_server",
    "controller_server",
    "behavior_server",
    "smoother_server",
    "map_server",
    "amcl",
    "velocity_smoother"
]

# script_dir = os.path.dirname(os.path.abspath(__file__))
# results_dir = os.path.join(script_dir, "results")
results_dir = os.path.expanduser("~/ros2_ws/results")
os.makedirs(results_dir, exist_ok=True)

# Output CSV
filename = os.path.join(results_dir, f"nav2_cpu_usage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

def find_nav2_processes():
    """Find all running Nav2 processes by name."""
    processes = {}
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in NAV2_PROCESSES:
            processes[proc.info['name']] = proc
    return processes

# Graceful stop flag
running = True
def handle_sigint(signum, frame):
    global running
    print("\nSIGINT received, stopping logging...")
    running = False

signal.signal(signal.SIGINT, handle_sigint)

def main(interval=1):
    processes = find_nav2_processes()
    print(f"Tracking {len(processes)} Nav2 processes. Logging...")

    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = ['timestamp'] + list(processes.keys())
        writer.writerow(header)

        for proc in processes.values():
            proc.cpu_percent(interval=None)

        while running:
            row = [datetime.now().isoformat()]
            for name, proc in processes.items():
                try:
                    cpu = proc.cpu_percent(interval=None)
                    row.append(round(cpu, 2))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    row.append('N/A')
            writer.writerow(row)
            f.flush()
            time.sleep(interval)

    print(f"Finished logging to {filename}")

if __name__ == "__main__":
    main()
