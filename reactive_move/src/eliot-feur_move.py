#!/usr/bin/python3
from rclpy.node import Node
import rclpy, math
from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header


class FonctionnementNormal:


    #____________________________________________________________________________

    def cloud_callback(self, nuage):
        elisabethBornX = 0.75
        elisabethBornY = 0.75
        pointPanik = None
        for pointNuage in nuage:
            if - elisabethBornX < pointNuage[0] < elisabethBornX:
                if - elisabethBornY < pointNuage[1] < elisabethBornY:
                    pointPanik = pointNuage
                    print("AHHHHHHHHHHHHHH")
        if pointPanik is None:
            print("panik IS NO MORE")
            print("tourner tout droit")
            rclpy.spin_once( myNode, timeout_sec=0.1 )
            velo = Twist()
            velo.linear.x= 0.2  # meter per second
            velo.angular.z= 0.0 # radian per second
            velocity_publisher.publish(velo)
        else:
            if pointPanik[0]<0:
                print("tourner à droite")
                rclpy.spin_once( myNode, timeout_sec=0.1 )
                velo = Twist()
                velo.linear.x= 0.2  # meter per second
                velo.angular.z= 0.2 # radian per second
                velocity_publisher.publish(velo)
            else:
                print("tourner à gauche")
                clpy.spin_once( myNode, timeout_sec=0.1 )
                velo = Twist()
                velo.linear.x= 0.2  # meter per second
                velo.angular.z= -0.2 # radian per second
                velocity_publisher.publish(velo)


    def process(self):
        rclpy.init(args=args)
        self._node = Node()
        self._node.create_subscription(LaserScan, 'cloud', self.cloud_callback, 10)
        
        ecrire topic tourne 

        # Infinite loop:
        rclpy.spin(minimal_subscriber)
        # Clean stop:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()



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