import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point32
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header


print("coucou")
rosNode= None

def scan_callback(scanMsg):
    global rosNode
    print(scanMsg.header)
    print(len(scanMsg.ranges))
    print("---------------------------------------------------------")
    #TROUVER COMMENT PUBLISH
    rosNode.publisher_.publish(cloudpublisher)
    

def convert_msg(scanMsg):
    obstacles= []
    angle= scanMsg.angle_min
    for aDistance in scanMsg.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [
                math.cos(angle) * aDistance,
                math.sin(angle) * aDistance
            ]
            obstacles.append(aPoint)
        angle+= scanMsg.angle_increment
    return obstacles

def arrondir(obstacles):
    sample= [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[10:20] ]
    rosNode.get_logger().info( f" obs({len(obstacles)}) ...{sample}..." )
    return sample

#le but est de créer un point cloud avec cette fonction, le heaeder est laser car c'est le repere dont sonyt tirés les obstacles
def point_cloud(scanMsg): 
    sample=arrondir(convert_msg(scanMsg))
    pointcloud = point_cloud2.create_cloud_xyz32(Header(frame_id='laser'), sample)
    for point in point_cloud2.read_points(pointcloud):
        print(point)


rclpy.init()
rosNode= Node('scan_interpreter')
rosNode.create_subscription( LaserScan, 'scan', scan_callback, 10)
cloudpublisher = rosNode.create_publisher(point_cloud2, 'cloud', point_cloud, 10)

while True :
    rclpy.spin_once( rosNode )

scanInterpret.destroy_node()
rclpy.shutdown()