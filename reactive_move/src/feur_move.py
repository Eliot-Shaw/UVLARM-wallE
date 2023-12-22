import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
# Message to publish:
from geometry_msgs.msg import Twist


class CloudToDecision(Node):

    def decision_callback(self, scanner): 
        self.publish(velo)
        pass
    
    def process(self):
        rclpy.init()
        #LA QUESTION EST POURQUOI LE _node 
        self._node = Node('decider_direction')               
        self._node.create_subscription(PointCloud2, 'cloud', self.decision_callback, 10)
        self._node.create_publisher(Twist, '/cmd_vel', 10)
        # Infinite loop:
        rclpy.spin(self)
        # Clean stop:
        self.destroy_node()
        rclpy.shutdown()

def main():
    minimal_subscriber= CloudToDecision()
    minimal_subscriber.process()