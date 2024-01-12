#!/usr/bin/python3

# This file gets laser streams topic in and publishes in /nuage topic

import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header


rosNode= None

def scan_callback(scanMsg):
    global rosNode
    print("---------------------------------------------------------")
    #TROUVER COMMENT PUBLISH
    cloudpublisher.publish(pointcloud(scanMsg))
    print("---------------------------------------------------------")
    

def convert_msg(scanMsg):
    obstacles= []
    angle= scanMsg.angle_min
    print(angle)
    for aDistance in scanMsg.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [
                math.cos(angle) * aDistance,
                math.sin(angle) * aDistance,
                0
            ]
            obstacles.append(aPoint)
        angle+= scanMsg.angle_increment
    return obstacles

def arrondir(obstacles):
    sample= [ [ round(p[0], 2), round(p[1], 2), 0 ] for p in  obstacles[10:20] ]
    rosNode.get_logger().info( f" obs({len(obstacles)}) ...{sample}..." )
    return sample

def pointcloud(scanMsg):
    pointlist = convert_msg(scanMsg)
    pointcloud = point_cloud2.create_cloud_xyz32(Header(frame_id='frame'), pointlist)
    compteur = 0
    for point in point_cloud2.read_points(pointcloud):
        print(point)
        compteur += 1
    print(f"Longueur totale : {compteur} ; sur scanMsg : {len(scanMsg.ranges)}")
    return pointcloud

rclpy.init()
rosNode= Node('scan_interpreter')
rosNode.create_subscription( LaserScan, 'scan', scan_callback, 10)
cloudpublisher = rosNode.create_publisher(PointCloud2, 'cloud', 10)

while True :
    rclpy.spin_once(rosNode)

scanInterpret.destroy_node()
rclpy.shutdown()

