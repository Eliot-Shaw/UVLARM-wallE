#!/usr/bin/env python3

import numpy as np
import cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from geometry_msgs.msg import Point, Pose
from visualization_msgs.msg import Marker, MarkerArray

class Marker_Array(Node):
    def __init__(self, fps= 60):
        super().__init__('marker_array')
        self.marker_array = MarkerArray()


    def add_marker_array(self, marker_bouteille):
        print(f"entrer marker_array")
        added = False
        # Iterate through existing markers in the array
        for existing_marker in self.marker_array:
            # Calculate the distance between marker_bouteille and existing_marker
            distance = distance_pose(marker_bouteille.pose, existing_marker.pose)

            # If the distance is less than 0.1, update the marker's position to the average
            if distance < 0.1:
                existing_marker.pose = moyenne_pose(marker_bouteille.pose, existing_marker.pose)
                print(f"Updated marker position based on average distance: {existing_marker.pose}")
                added = True
                break

        if not added:
            self.marker_array.append(marker_bouteille)
            print(f"Added a new marker to the array: {marker_bouteille}")

        # Publish the updated MarkerArray
        self.publisher_marker_array.publish(self.marker_array)
        print(f"Publish marker array ------------ {self.marker_array}")


    def distance_pose(pose1, pose2):
        x1, y1, z1 = pose1.position.x, pose1.position.y, pose1.position.z
        x2, y2, z2 = pose2.position.x, pose2.position.y, pose2.position.z
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        return distance


    def moyenne_pose(pose1, pose2):
        x1, y1, z1 = pose1.position.x, pose1.position.y, pose1.position.z
        x2, y2, z2 = pose2.position.x, pose2.position.y, pose2.position.z

        moy_pose = Pose()

        moy_pose.position.x = (x1 + x2) / 2.0
        moy_pose.position.y = (y1 + y2) / 2.0
        moy_pose.position.z = (z1 + z2) / 2.0
        moy_pose.orientation.x = (pose1.orientation.x + pose2.orientation.x) / 2.0
        moy_pose.orientation.y = (pose1.orientation.y + pose2.orientation.y) / 2.0
        moy_pose.orientation.z = (pose1.orientation.z + pose2.orientation.z) / 2.0
        moy_pose.orientation.w = (pose1.orientation.w + pose2.orientation.w) / 2.0

        return moy_pose


    def work(self):
        print("on va partir dans subscribe&publish")
        self.create_subscription(Marker, '/marker_bouteille', self.add_marker_array, 10) 
        self.publisher_marker_array = self.create_publisher(MarkerArray, '/map', 10)
        print("subscribe&publish ok")
        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)

def main():
    print("depth")
    rclpy.init()
    minimal_subscriber = Marker_Array()
    print("initialisation : ok")
    minimal_subscriber.work()

if __name__ == '__main__':
# call main() function
    main()