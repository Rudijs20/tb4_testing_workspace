import subprocess
import time
import os
import signal
import sys

NUM_RUNS = 9
WORLD_DIR = "/opt/ros/jazzy/share/turtlebot4_gz_bringup/worlds"

sim_proc = None
nav_proc = None

def signal_handler(sig, frame):
    print("\nCaught Ctrl+C! Shutting down...")

    # First close nav_proc if running
    global nav_proc
    if nav_proc and nav_proc.poll() is None:
        print("Terminating nav_to_pose...")
        nav_proc.terminate()
        try:
            nav_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            nav_proc.kill()

    # Then close sim_proc if running
    global sim_proc
    if sim_proc and sim_proc.poll() is None:
        print("Terminating simulation...")
        sim_proc.terminate()
        os.killpg(os.getpgid(sim_proc.pid), signal.SIGINT)
        try:
            sim_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            sim_proc.kill()

    print("Shutdown complete.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

for i in range(NUM_RUNS):
    print(f"\n--- Run {i+1}/{NUM_RUNS} ---")

    sim_proc = subprocess.Popen([
        "ros2", "launch", "turtlebot4_gz_bringup", "turtlebot4_gz.launch.py",
        "nav2:=true",
        "slam:=false",
        "localization:=true",
        "rviz:=false",
        "use_sim_time:=true",
        "world:=maze",
        "map:=/opt/ros/jazzy/share/turtlebot4_navigation/maps/maze.yaml",
        "x:=1.7502",
        "y:=-0.2405",
        "yaw:=0.45"
    ], cwd=WORLD_DIR,
       preexec_fn=os.setsid
    )

    print("Simulation launching...")

    time.sleep(15)

    nav_proc = subprocess.Popen([
        "ros2", "run", "tb4_nav_to_pose", "nav_to_pose"
    ])

    nav_proc.wait()
    print("Navigation completed.")

    # Kill simulation after navigation
    if sim_proc.poll() is None:
        sim_proc.terminate()
        os.killpg(os.getpgid(sim_proc.pid), signal.SIGINT)
        try:
            sim_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            sim_proc.kill()

    time.sleep(5)

print("\n✅ All runs completed.")
