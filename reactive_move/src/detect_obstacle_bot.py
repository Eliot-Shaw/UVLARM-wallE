#!/usr/bin/python3
import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
# Message to publish:
from geometry_msgs.msg import Twist


class CloudToDecision(Node):

    def cloud_callback(self, nuage): #fonction de décision
        #bornes de détections absolues en mètres
        borneX = 0.7 #devant le robot
        borneY = 0.3
        pointObstacle = None
        for pointNuage in point_cloud2.read_points(nuage):
            #si point est dans le carré
            if -borneY < pointNuage[1] < borneY:
                if 0 < pointNuage[0] < borneX:
                    #on trouve le point de décision = point le + proche du robot
                    #comparer dist point obstacle avec point nuage
                    if (pointObstacle is None) or (math.sqrt(pointObstacle[0]*pointObstacle[0]+pointObstacle[1]*pointObstacle[1])>math.sqrt(pointNuage[0]*pointNuage[0]+pointNuage[1]*pointNuage[1])):
                        pointObstacle = pointNuage
                    
        if pointObstacle is None:
            print("tourner tout droit")
            velo = Twist()
            velo.linear.x= 0.5   # meter per second
            velo.angular.z= 0.0 # radian per second
        else:
            print(f"x : {pointObstacle[0]} ; y: {pointObstacle[1]}")
            if pointObstacle[1]<0:
                print("tourner à droite")
                velo = Twist()
                velo.linear.x= 0.0  # meter per second
                velo.angular.z= 0.5 # radian per second
            else:
                print("tourner à gauche")
                velo = Twist()
                velo.linear.x= 0.0  # meter per second
                velo.angular.z= -0.5 # radian per second
                
        self.publisher_.publish(velo)
        
    
    def process(self):
        #rclpy.init()
        #LA QUESTION EST POURQUOI LE _node              
        self.create_subscription(PointCloud2, 'cloud', self.cloud_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/multi/cmd_nav', 10)  #/cmd_vel pour simu ; /multi/cmd_nav pour tbot
        rclpy.spin(self)
        self.destroy_node()
        rclpy.shutdown()

def main():
    rclpy.init()
    minimal_subscriber= CloudToDecision('decider_direction')
    minimal_subscriber.process()

if __name__ == '__main__':
# call main() function
    main()