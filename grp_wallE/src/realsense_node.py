#!/usr/bin/env python3

import pyrealsense2 as rs
import signal, time, numpy as np
import sys, cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

isOk= True

# Realsense Node:
class Realsense(Node):
    def __init__(self, fps= 60):
        super().__init__('realsense')

        self.pipeline = rs.pipeline()
        self.config = rs.config()


    def start_connexion(self):
        # Configure depth, infrared and color streams

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

        self.config.enable_stream(rs.stream.infrared, 1, 848, 480, rs.format.y8, 60)
        self.config.enable_stream(rs.stream.infrared, 2, 848, 480, rs.format.y8, 60)


    def read_imgs(self):
        # Wait for a coherent tuple of frames: depth, color and accel
        frames = self.pipeline.wait_for_frames()

        color_frame = frames.first(rs.stream.color)
        depth_frame = frames.first(rs.stream.depth)

        self.infra_frame_1 = frames.get_infrared_frame(1)
        self.infra_frame_2 = frames.get_infrared_frame(2)
        
        if not (depth_frame and color_frame and self.infra_frame_1 and self.infra_frame_2):
            pass


        # Convert images to numpy arrays
        self.depth_image = np.asanyarray(depth_frame.get_data())
        self.color_image = np.asanyarray(color_frame.get_data())

        self.infra_image_1 = np.asanyarray(self.infra_frame_1.get_data())
        self.infra_image_2 = np.asanyarray(self.infra_frame_2.get_data())

        # Utilisation de colormap sur l'image infrared de la Realsense (image convertie en 8-bit par pixel)
        self.infra_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(self.infra_image_1, alpha=1), cv2.COLORMAP_JET)
            
        # Utilisation de colormap sur l'image infrared de la Realsense (image convertie en 8-bit par pixel)
        self.infra_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(self.infra_image_2, alpha=1), cv2.COLORMAP_JET)	
        
        
    def publish_imgs(self):
        self.bridge=CvBridge()
        msg_image = self.bridge.cv2_to_imgmsg(self.color_image,"bgr8")
        msg_image.header.stamp = self.get_clock().now().to_msg()
        msg_image.header.frame_id = "image"
        self.image_image_publisher.publish(msg_image)

        # Utilisation de colormap sur l'image depth de la Realsense (image convertie en 8-bit par pixel)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)
        msg_depth = self.bridge.cv2_to_imgmsg(depth_colormap,"bgr8")
        msg_depth.header.stamp = msg_image.header.stamp
        msg_depth.header.frame_id = "depth"
        self.image_depth_publisher.publish(msg_depth)

        # Infrared
        msg_infra = self.bridge.cv2_to_imgmsg(self.infra_colormap_1,"bgr8")
        msg_infra.header.stamp = msg_image.header.stamp
        msg_infra.header.frame_id = "infrared_1"
        self.infra_publisher_1.publish(msg_infra)

        msg_infra = self.bridge.cv2_to_imgmsg(self.infra_colormap_2,"bgr8")
        msg_infra.header.stamp = msg_image.header.stamp
        msg_infra.header.frame_id = "infrared_2"
        self.infra_publisher_2.publish(msg_infra)



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
        self.image_image_publisher = self.create_publisher(Image, '/image_image', 10)
        self.image_depth_publisher = self.create_publisher(Image, '/image_depth', 10)


        self.infra_publisher_1 = self.create_publisher(Image, '/infrared_1', 10) 
        self.infra_publisher_2 = self.create_publisher(Image, '/infrared_2', 10)


        
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