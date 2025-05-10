import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException

from std_msgs.msg import Int32
from std_srvs.srv import Trigger

class CounterPublisher(Node):

    def __init__(self):
        super().__init__('counter_publisher')
        self.publisher_ = self.create_publisher(Int32, 'counter_topic', 10)
        
        # Get timer_period parameter with default value of 1.0 seconds
        self.declare_parameter('timer_period', 1.0)
        timer_period = self.get_parameter('timer_period').get_parameter_value().double_value
        
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0

        # Get counter_max parameter with default value of 10
        self.declare_parameter('counter_max', 10)
        self.counter_max = self.get_parameter('counter_max').get_parameter_value().integer_value
        self.get_logger().info(f'Counter created with max value ({self.counter_max}) and timer period {timer_period}s')
        
        # Create a service to reset the counter
        self.service = self.create_service(
            srv_type=Trigger,
            srv_name='reset_counter',
            callback=self.reset_counter_callback,
        )

    def reset_counter_callback(self, request, response):
        self.counter = 0
        self.get_logger().info('Counter has been reset')
        response.success = True
        response.message = 'Counter has been reset'
        return response


    def timer_callback(self):
        msg = Int32()
        msg.data = self.counter
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {self.counter}')
        self.counter += 1
        
        # Check if we've reached the counter limit
        if self.counter >= self.counter_max:
            self.get_logger().info(f'Counter limit reached ({self.counter_max}), shutting down...')
            self.timer.cancel()
            exit()


def main(args=None):
    rclpy.init(args=args)

    node = CounterPublisher()

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
