import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from rclpy.executors import ExternalShutdownException

class CounterSubscriber(Node):
    def __init__(self):
        super().__init__('counter_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'counter_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = CounterSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
