# TurtleBot4 Navigation Workspace

This workspace contains the packages for running both simulation and real-world tests.

## Building the Workspace

Run the following command inside the `ros2_ws` folder (**must be located in your home directory**, otherwise the scripts won’t work):

```bash
colcon build --symlink-install
```

> `--symlink-install` allows Python packages to be used without needing to rebuild after code edits.

---

## Running Simulation Tests

To run simulation tests, execute:

```bash
python3 repeat_test.py
```

This will automatically launch:

* `battery_logger`
* `cmd_vel_logger`
* `nav2_cpu_logger.py`
* `nav_metrics_logger`

There’s also a lightweight `min_nav_to_pose` script that only activates the initial pose and goal position, without logging any metrics.

---

## Logging Local Planner Behavior

To count how often the local planner makes changes, you’ll need to **manually update the subscriber topic** in `nav_to_pose.py`.

There are comments in the nav_to_pose.py file explaining which topic to use for each controller.

---

## Changing Navigation Controllers

To switch the navigation controller or planner, edit:

```bash
~/ros2_ws/src/turtlebot4-jazzy/turtlebot4_navigation/config/nav2.yaml
```

* The **RPP controller plugin** is placed under the `FollowPath` section.
* To use a different controller, replace the whole section under `FollowPath`.
* Good example configurations:
  [https://docs.nav2.org/configuration/index.html](https://docs.nav2.org/configuration/index.html)

---

## Running Real-World Tests

Real-world tests require several processes to be started manually due to frequent crashes and general instability.

First repeat the colcon build steps from the simulation setup

Run these commands in this order:

### On SSH'ed terminal (except step 3):

1. File already located on the turtlebot at VU

```bash
ros2 launch turtlebot4_navigation localization.launch.py map:=/home/ubuntu/FullMap5.2.yaml
```

2.

```bash
ros2 launch turtlebot4_navigation nav2.launch.py
```

3. *(Run locally, **not over SSH**)*:

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py
```

4.

```bash
python3 nav2_cpu_logger.py
```

5.

```bash
ros2 run tb4_nav_to_pose realW_nav_to_pose
```

---

## 🧪 Configs Used for Thesis Testing

### ⚒️ Regulated Pure Pursuit (RPP)

```yaml
plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
desired_linear_vel: 0.5
max_angular_accel: 3.2
rotate_to_heading_angular_vel: 1.9
transform_tolerance: 0.1
allow_reversing: false
use_rotate_to_heading: true
rotate_to_heading_min_angle: 0.785
stateful: true
```

---

### ⚙️ DWB

```yaml
plugin: "dwb_core::DWBLocalPlanner"
max_vel_x: 0.5
min_vel_x: 0.0
max_vel_theta: 1.9
min_speed_xy: 0.0
max_speed_xy: 0.5
min_speed_theta: 0.0
acc_lim_x: 2.5
acc_lim_theta: 3.2
decel_lim_x: -2.5
decel_lim_theta: -3.2
vx_samples: 20
vtheta_samples: 20
sim_time: 1.7
linear_granularity: 0.05
angular_granularity: 0.025
transform_tolerance: 0.1
xy_goal_tolerance: 0.25
trans_stopped_velocity: 0.25
short_circuit_trajectory_evaluation: true
limit_vel_cmd_in_traj: false
stateful: true
allow_reverse: false
critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
```

---

### 🧠 MPPI

```yaml
plugin: "nav2_mppi_controller::MPPIController"
time_steps: 32
model_dt: 0.05
batch_size: 2000
vx_max: 0.5
vx_min: 0.0
wz_max: 1.9
wz_min: -1.9
ax_max: 3.0
ax_min: -3.0
vx_std: 0.2
vy_std: 0.0
wz_std: 0.3
timeout: 0.1
goal_dist_tol: 0.25
transform_tolerance: 0.1
temperature: 0.3
gamma: 0.015
motion_model: "DiffDrive"
visualize: false
reset_period: 1.0
prune_distance: 1.7
use_critic_evaluation: false
allow_reverse: false
stateful: true
regenerate_noises: true
iteration_count: 1
critics: [
       "ConstraintCritic", "CostCritic", "GoalCritic",
       "GoalAngleCritic", "PathAlignCritic", "PathFollowCritic",
       "PathAngleCritic", "PreferForwardCritic"
   	    ]
```
