#!/usr/bin/env python3

import numpy as np
import cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

message = Float32()

# Node Profondeur couleur verte:
class Profondeur(Node):
    def __init__(self, fps= 60):
        super().__init__('profondeur')

    def lastImg (self, image_depth_sub):
        bridge = CvBridge()
        self.cv2_image_depth = bridge.imgmsg_to_cv2(img_msg=image_depth_sub, desired_encoding='passthrough')

    def profondeur(self, coords_sub):
        print("on va partir dans ok")
        message.data = self.cv2_image_depth.get_distance(coords_sub.x, coords_sub.y)
        self.publisher_distance_bouteille.publish(message)
        print(f"lastImg ok ------------ {message}")


    def process_img(self):
        print("on va partir dans subscribe&publish")
        self.create_subscription(Image, '/image_depth', self.lastImg, 10) 
        self.create_subscription(Image, '/coords_img_bouteille', self.profondeur, 10) 
        self.publisher_distance_bouteille = self.create_publisher(Float32, '/distance_bouteille', 10)
        self.publisher_distance_bouteille.publish(0.0)
        print("subscribe&publish ok")

        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)
        
        imgmsg_cap.release()
        cv2.destroyAllWindows()


def main():
    rclpy.init()
    minimal_subscriber= Profondeur()
    print("initialisation : ok")
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()