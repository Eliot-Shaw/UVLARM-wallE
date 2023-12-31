import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

rosNode= None

def scan_callback(scanMsg):
    global rosNode
    #rosNode.get_logger().info( f"scan:\n{scanMsg}" )
    print(scanMsg.header)
    print(len(scanMsg.ranges))
    print("---------------------------------------------------------")


rclpy.init()
rosNode= Node('scan_interpreter')
rosNode.create_subscription( LaserScan, 'scan', scan_callback, 10)

while True :
    rclpy.spin_once( rosNode )
scanInterpret.destroy_node()
rclpy.shutdown()