import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import os
from datetime import datetime
import signal

class CmdVelLogger(Node):
    def __init__(self):
        super().__init__('cmd_vel_logger')

        self.results_dir = os.path.expanduser("~/ros2_ws/results")
        os.makedirs(self.results_dir, exist_ok=True)

        self.filename = f"cmd_vel_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.file_path = os.path.join(self.results_dir, self.filename)

        self.log_file = open(self.file_path, 'w', newline='')
        self.log_file.write("realtime,timestamp,linear_x,linear_y,linear_z,angular_x,angular_y,angular_z\n")
        self.get_logger().info(f"Logging to: {self.file_path}")

        self.subscription = self.create_subscription(
            TwistStamped,
            '/cmd_vel',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        realtime = datetime.now().isoformat()

        line = f"{realtime},{timestamp}," \
               f"{msg.twist.linear.x},{msg.twist.linear.y},{msg.twist.linear.z}," \
               f"{msg.twist.angular.x},{msg.twist.angular.y},{msg.twist.angular.z}\n"

        self.log_file.write(line)
        self.log_file.flush()

    def destroy_node(self):
        self.log_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelLogger()

    def shutdown_handler(signum, frame):
        node.get_logger().info("SIGINT received, stopping logging...")
        rclpy.shutdown()

    signal.signal(signal.SIGINT, shutdown_handler)

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()

if __name__ == '__main__':
    main()
