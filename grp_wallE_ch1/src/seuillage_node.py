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


    def souris(event, x, y, flags, param):
        global lo, hi, color, hsv_px

        if event == cv2.EVENT_MOUSEMOVE:
            # Conversion des trois couleurs RGB sous la souris en HSV
            px = frame[y,x]
            px_array = np.uint8([[px]])
            hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)

        if event==cv2.EVENT_MBUTTONDBLCLK:
            color=image[y, x][0]

        if event==cv2.EVENT_LBUTTONDOWN:
            if color>5:
                color-=1

        if event==cv2.EVENT_RBUTTONDOWN:
            if color<250:
                color+=1

        lo[0]=color-10
        hi[0]=color+10


    def read_imgs(self):
        pass

    def publish_img(self):
        pass

    def process_img(self):
        self.create_subscription(Image, '/image_image', self.process_img(), 10) ###BONNNE QUESTION MON REUF###
        self.publisher_ = self.create_publisher(Image, '/bonnequestion', 10) 

        color=60 # HSV : detecter H = 60 (vert vert)

        lo=np.array([color-5, 100, 50])
        hi=np.array([color+5, 255,255])

        color_info=(0, 0, 255)

        cap=cv2.VideoCapture(0)
        cv2.namedWindow('Camera')
        cv2.setMouseCallback('Camera', souris)
        hsv_px = [0,0,0]

        # Creating morphological kernel
        kernel = np.ones((3, 3), np.uint8)

        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)

def main():
    rclpy.init()
    minimal_subscriber= Seuillage()
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()