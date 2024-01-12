#!/usr/bin/env python3

import pyrealsense2 as rs
import signal, time, numpy as np
import sys, cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# Node Seuillage couleur verte:
class Seuillage(Node):
    def __init__(self, fps= 60):
        super().__init__('seuillage')


    def start_connexion(self):
        pass

    def read_imgs(self):
        pass

    def publish_img(self):
        pass

    def process_img(self):
        pass

