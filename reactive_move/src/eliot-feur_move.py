#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class FonctionnementNormal:
    def scan_callback(self, nuage):
        if nuage == []:
            ecrire que tout va bien
        else :
            tout va mal, bouger

    def process(self):
        subscription topic scan
        Nodepublisher pour avancer normalement
        spin



class MSContext():

    def listener_callback(self, msg):
        self._node.get_logger().info('I heard: "%s"' % msg.data)
    
    def process(self)
        rclpy.init(args=args)
        self._node = Node()
        self._node.create_subscription(
            String, 'topic',
            self.listener_callback, 10)
        # Infinite loop:
        rclpy.spin(minimal_subscriber)
        # Clean stop:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()