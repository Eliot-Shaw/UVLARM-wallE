#!/usr/bin/python3

# This file subscribes to /nuage topic in and publishes in /multi/cmd_vel topic

import rclpy, math
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from geometry_msgs.msg import Twist


class CloudToDecision(Node):
    def __init__(self):
        super().__init__('decider_direction')
        self.ordre_date_executive = None

    def cloud_callback(self, nuage): #fonction de décision
        #bornes de détections absolues en mètres
        borneX = 0.7 #devant le robot
        borneY = 0.28
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
            print("Pas d'obstacle: on avance tout droit")
            velo = Twist()
            velo.linear.x= 0.3   # meter per second
            velo.angular.z= 0.0 # radian per second
            self.publisher_.publish(velo)
        else:
            if pointObstacle[0] < 0.3:
                print("Obstacle trop proche !! Arrêt puis changement de direction")
                velo = Twist()
                velo.linear.x= 0.0   # meter per second
                velo.angular.z= 0.5 # radian per second
                self.publisher_.publish(velo)
            else:
                if pointObstacle[1]<0:
                    print("Obstacle distant à gauche: on tourne à droite")
                    velo = Twist()
                    velo.linear.x= 0.3  # meter per second
                    velo.angular.z= 1.5 # radian per second
                    self.publisher_.publish(velo)
                else:
                    print("Obstacle distant à droite: on tourne à gauche")
                    velo = Twist()
                    velo.linear.x= 0.3   # meter per second
                    velo.angular.z= -1.5 # radian per second
                    self.publisher_.publish(velo)

            
        
    
    def process(self):             
        self.create_subscription(PointCloud2, 'cloud', self.cloud_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/multi/cmd_nav', 10)  #/cmd_vel pour simu ; /multi/cmd_nav pour tbot
        rclpy.spin(self)
        self.destroy_node()
        rclpy.shutdown()

def main():
    rclpy.init()
    minimal_subscriber= CloudToDecision()
    minimal_subscriber.process()

if __name__ == '__main__':
# call main() function
    main()