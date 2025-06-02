import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
import os
from datetime import datetime
import signal

class BatteryLogger(Node):
    def __init__(self):
        super().__init__('battery_logger')

        self.results_dir = os.path.expanduser("~/ros2_ws/results")
        os.makedirs(self.results_dir, exist_ok=True)

        self.filename = f"battery_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.file_path = os.path.join(self.results_dir, self.filename)
        
        self.log_file = open(self.file_path, 'w', newline='')
        self.log_file.write('realtime,time,voltage,current\n')
        self.get_logger().info(f"Logging to: {self.file_path}")

        self.subscription = self.create_subscription(
            BatteryState,
            '/battery_state',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        realtime = datetime.now().isoformat()
        self.log_file.write(f'{realtime},{timestamp},{msg.voltage},{msg.current}\n')
        self.log_file.flush()

    def destroy_node(self):
        self.log_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = BatteryLogger()

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
