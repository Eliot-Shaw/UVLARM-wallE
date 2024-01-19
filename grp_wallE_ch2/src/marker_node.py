#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf2_geometry_msgs
import time

class MarkerBouteille(Node):
    def __init__(self, fps=60):
        super().__init__('marker_bouteille')
        self.marker_bouteille = Marker()
        self.tf_buffer = Buffer()  # tf buffer length
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def create_marker_bouteille(self, point_bouteille):
        print(f"entrer create_marker_bouteille")
        bouteille_pose = Pose()
        bouteille_pose.position.x = point_bouteille.x
        bouteille_pose.position.y = point_bouteille.y
        bouteille_pose.position.z = point_bouteille.z
        
        bouteille_pose.orientation.x = 0.0  # À remplir
        bouteille_pose.orientation.y = 0.0
        bouteille_pose.orientation.z = 0.0
        bouteille_pose.orientation.w = 0.0

        try:
            self.transform_baselink_map = self.tf_buffer.lookup_transform(target_frame="map", source_frame="base_link", time=time.time())
            bouteille_pose_transformed = tf2_geometry_msgs.do_transform_pose(bouteille_pose, self.transform_baselink_map)
        except Exception as e:
            print(f'Error transforming point: {e}')
            return

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rclpy.Time.now()

        marker.type = 3  # cylindre

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
        marker.pose = bouteille_pose_transformed.pose

        self.publisher_marker_bouteille.publish(marker)

    def work(self):
        print("on va partir dans subscribe&publish")
        self.create_subscription(Point, '/point_bouteille', self.create_marker_bouteille, 10) 
        self.publisher_marker_bouteille = self.create_publisher(Marker, '/marker_bouteille', 10)
        print("subscribe&publish ok")
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.001)

def main():
    print("marker_node")
    rclpy.init()
    minimal_subscriber = MarkerBouteille()
    print("initialisation : ok")
    minimal_subscriber.work()

if __name__ == '__main__':
    # call main() function
    main()
