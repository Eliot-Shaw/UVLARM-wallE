#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Point, Pose
from visualization_msgs.msg import Marker
import tf2_ros
import tf2_geometry_msgs
import rospy

class Marker_Bouteille(Node):
    def __init__(self, fps= 60):
        super().__init__('marker_bouteille')
        self.marker_bouteille = Marker()
        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

    def marker_bouteille(self, point_bouteille):
        print(f"entrer marker_bouteille")
        bouteille_pose = Pose()
        bouteille_pose.position.x = point_bouteille.x
        bouteille_pose.position.y = point_bouteille.y
        bouteille_pose.position.z = point_bouteille.z
        
        bouteille_pose.orientation.x = 0.0 #sais pas encore
        bouteille_pose.orientation.y = 0.0
        bouteille_pose.orientation.z = 0.0
        bouteille_pose.orientation.w = 0.0

        self.transform_baselink_map = self.tf_buffer.lookup_transform("map", "base_link", point_bouteille.header.stamp, rospy.Duration(1.0))
                                                                                #rospy.Time.now() si marche pas

        self.bouteille_pose_transformed = tf2_geometry_msgs.do_transform_pose(bouteille_pose, self.transform_baselink_map)

        marker = Marker()
        
        marker.header.frame_id = "map"
        marker.header.stamp = self.bouteille_pose_transformed.header.stamp #point_bouteille.header.stamp ou rospy.Time.now() si marche pas

        marker.type = 3 # = cylindre

        # Taille 
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.17

        # Couleur GRBA
        marker.color.r = 1.0  
        marker.color.g = 0.0  
        marker.color.b = 0.0  
        marker.color.a = 1.0  # Alpha (transparence)

        # Set the pose of the marker based on the transformed pose
        marker.pose = self.bouteille_pose_transformed.pose



    def work(self):
        print("on va partir dans subscribe&publish")
        self.create_subscription(Point, '/point_bouteille', self.marker_bouteille, 10) 
        self.publisher_marker_bouteille = self.create_publisher(Marker, '/marker_bouteille', 10)
        print("subscribe&publish ok")
        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)

def main():
    print("depth")
    rclpy.init()
    minimal_subscriber = Marker_Bouteille()
    print("initialisation : ok")
    minimal_subscriber.work()

if __name__ == '__main__':
# call main() function
    main()
