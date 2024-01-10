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
        # Wait for a coherent tuple of frames: depth, color and accel
        frames = self.pipeline.wait_for_frames()

        color_frame = frames.first(rs.stream.color)
        depth_frame = frames.first(rs.stream.depth)
        
        if not (depth_frame and color_frame):
            pass

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        sys.stdout.write( f"\r- {color_colormap_dim} - {depth_colormap_dim} - ({round(self.freq)} fps)" )
        # Show images
        images = np.hstack((color_image, depth_colormap))
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

    def publish_imgs(self):
        pass

    # Capture ctrl-c event
    def signalInteruption(signum, frame):
        global isOk
        print( "\nCtrl-c pressed" )
        isOk= False
    signal.signal(signal.SIGINT, signalInteruption)

    def process_img(self):
        self.start_connexion()
        # Start streaming
        self.pipeline.start(self.config)
        count= 1
        refTime= time.process_time()
        self.freq= 60
        sys.stdout.write("-")
        while isOk:
            self.read_imgs()
            self.publish_imgs()
            # Frequency:
            if count == 10 :
                newTime= time.process_time()
                self.freq= 10/((newTime-refTime))
                refTime= newTime
                count= 0
            count+= 1
            rclpy.spin_once(self, timeout_sec=0.001)
        # Stop streaming
        print("Ending...")
        self.pipeline.stop()
        # Clean end
        self.destroy_node()
        rclpy.shutdown()
    
def main():
    rclpy.init()
    minimal_subscriber= Realsense()
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()