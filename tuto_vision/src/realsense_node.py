#!/usr/bin/env python3

import pyrealsense2 as rs
import signal, time, numpy as np
import sys, cv2, rclpy
from rclpy.node import Node

isOk= True

# Realsense Node:
class Realsense(Node):
    def __init__(self, fps= 60):
        super().__init__('realsense')

        self.pipeline = rs.pipeline()
        self.config = rs.config()

    def start_connexion(self):
        # Configure depth and color streams

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        print( f"Connect: {device_product_line}" )
        found_rgb = True
        for s in device.sensors:
            print( "Name:" + s.get_info(rs.camera_info.name) )
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True

        if not (found_rgb):
            print("Depth camera equired !!!")
            exit(0)

        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)

    def read_imgs(self):
        pass

    def publish_imgs(self):
        pass

    # Capture ctrl-c event
    def signalInteruption(signum, frame):
        global isOk
        print( "\nCtrl-c pressed" )
        isOk= False
    signal.signal(signal.SIGINT, signalInteruption)

    def process_img(self):
        rsNode= Realsense()
        rsNode.start_connexion()
        # Start streaming
        self.pipeline.start(self.config)
        count= 1
        refTime= time.process_time()
        freq= 60
        sys.stdout.write("-")
        while isOk:
            rsNode.read_imgs()
            rsNode.publish_imgs()
            # Frequency:
            if count == 10 :
                newTime= time.process_time()
                freq= 10/((newTime-refTime))
                refTime= newTime
                count= 0
            count+= 1
            rclpy.spin_once(rsNode, timeout_sec=0.001)
        # Stop streaming
        print("Ending...")
        rsNode.pipeline.stop()
        # Clean end
        rsNode.destroy_node()
        rclpy.shutdown()
    
def main():
    rclpy.init()
    minimal_subscriber= Realsense()
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()