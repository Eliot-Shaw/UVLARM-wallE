#!/usr/bin/env python3

import pyrealsense2 as rs
import signal, time, numpy as np
import sys, cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
import math


isOk= True

# Realsense Node:
class Realsense(Node):
    def __init__(self, fps= 60):
        super().__init__('realsense')
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.colorizer = rs.colorizer()


    def start_connexion(self):
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
            print("Depth camera required !!!")
            exit(0)

        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)

        # Start streaming
        self.pipeline.start(self.config)

        align_to = rs.stream.depth
        self.align = rs.align(align_to)
        self.refTime = time.process_time()
        self.count= 1
        self.freq= 60

        #Visualisation point depth
        self.color_info = (0,0,255)
        self.rayon = 10



    def read_imgs(self):
        # Wait for a coherent tuple of frames: depth, color and accel
        frames = self.pipeline.wait_for_frames()

        aligned_frames = self.align.process(frames)
        self.depth_frame = aligned_frames.get_depth_frame()
        aligned_color_frame = aligned_frames.get_color_frame()

        if not self.depth_frame or not aligned_color_frame: pass

        # Convert images to numpy arrays
        self.depth_image = np.asanyarray(self.depth_frame.get_data())
        self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)
        self.color_image = np.asanyarray(aligned_color_frame.get_data())	

        # Get the intrinsic parameters
        self.color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
        self.depth_colormap_dim = self.depth_colormap.shape
        self.color_colormap_dim = self.color_image.shape

        
        
    def publish_imgs(self):
        self.bridge=CvBridge()
        msg_image = self.bridge.cv2_to_imgmsg(self.color_image,"bgr8")
        msg_image.header.stamp = self.get_clock().now().to_msg()
        msg_image.header.frame_id = "image"
        self.image_image_publisher.publish(msg_image)

        # Utilisation de colormap sur l'image depth de la Realsense (image convertie en 8-bit par pixel)
        msg_depth = self.bridge.cv2_to_imgmsg(self.depth_colormap,"bgr8")
        msg_depth.header.stamp = msg_image.header.stamp
        msg_depth.header.frame_id = "depth"
        self.image_depth_publisher.publish(msg_depth)


    def calcul_distance_bouteille(self, coords_bouteille):
        #Use pixel value of  depth-aligned color image to get 3D axes
        point_bouteille = Point()
        dist = Float32()
        depth = self.depth_frame.get_distance(int(coords_bouteille.x),int(coords_bouteille.y)) ####pb ici
        dx ,dy, dz = rs.rs2_deproject_pixel_to_point(self.color_intrin, [int(coords_bouteille.x),int(coords_bouteille.y)], depth)
        dist.data = math.sqrt(((dx)**2) + ((dy)**2) + ((dz)**2))

        point_bouteille.x = dx
        point_bouteille.z = dy
        point_bouteille.z = dz
        if dist.data > 0.15: #éviter les 0 quand le robot va trop vite
            self.dist_publisher.publish(dist)
            self.publisher_point_bouteille.publish(point_bouteille)
        

    # Capture ctrl-c event
    def signalInteruption(signum, frame):
        global isOk
        print( "\nCtrl-c pressed" )
        isOk= False
    signal.signal(signal.SIGINT, signalInteruption)


    def process_img(self):
        self.start_connexion()
        sys.stdout.write("-")

        self.create_subscription(Point, '/coords_img_bouteille', self.calcul_distance_bouteille, 10) 

        self.image_image_publisher = self.create_publisher(Image, '/image_image', 10)
        self.image_depth_publisher = self.create_publisher(Image, '/image_depth', 10)
        self.dist_publisher = self.create_publisher(Float32, '/distance_bouteille', 10)
        self.publisher_point_bouteille = self.create_publisher(Point, '/point_bouteille', 10)


        
        while isOk:
            self.read_imgs()
            self.publish_imgs()
            # Frequency:
            if self.count == 10 :
                newTime= time.process_time()
                self.freq= 10/((newTime-self.refTime))
                self.refTime= newTime
                self.count= 0
            self.count+= 1
            rclpy.spin_once(self, timeout_sec=0.001)
        # Stop streaming
        print("Ending...")
        self.pipeline.stop()
        # Clean end
        self.destroy_node()
        rclpy.shutdown()
    
def main():
    print("camera")
    rclpy.init()
    minimal_subscriber= Realsense()
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()