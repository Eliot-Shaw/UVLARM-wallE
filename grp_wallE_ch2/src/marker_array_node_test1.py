#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker, MarkerArray
import math

class Marker_Array(Node):
    def __init__(self, fps= 60):
        super().__init__('marker_array')
        self.marker_array = MarkerArray()


    def add_marker_array(self, marker_bouteille):
        print(f"entrer marker_array")
        
        self.marker_array.append(marker_bouteille)
        print(f"Added a new marker to the array: {marker_bouteille}")

        # Publish the updated MarkerArray
        self.publisher_marker_array.publish(self.marker_array)
        print(f"Publish marker array ------------ {self.marker_array}")


    def work(self):
        print("on va partir dans subscribe&publish")
        self.create_subscription(Marker, '/marker_bouteille', self.add_marker_array, 10) 
        self.publisher_marker_array = self.create_publisher(MarkerArray, '/marker_array_bouteille', 10)
        print("subscribe&publish ok")
        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)

def main():
    print("marker_array_node_test1, devrait marcher")
    rclpy.init()
    minimal_subscriber = Marker_Array()
    print("initialisation : ok")
    minimal_subscriber.work()

if __name__ == '__main__':
# call main() function
    main()