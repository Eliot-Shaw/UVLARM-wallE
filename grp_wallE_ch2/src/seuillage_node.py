#!/usr/bin/env python3

import numpy as np
import cv2, rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import Float32

message = Point()

# Node Seuillage couleur verte:
class Seuillage(Node):
    def __init__(self, fps= 60):
        super().__init__('seuillage')
        self.dist_bout = None


    def souris(self, event, x, y, flags, param):

        if event == cv2.EVENT_MOUSEMOVE:
            # Conversion des trois couleurs RGB sous la souris en HSV
            px = self.frame[y,x]
            px_array = np.uint8([[px]])
            self.hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)

    def seuillage(self, cap):
        self.bridge = CvBridge()
        self.frame = self.bridge.imgmsg_to_cv2(img_msg=cap, desired_encoding='passthrough')
        self.image=cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(self.image, self.lo, self.hi)
        # Flouttage de l'image
        self.image=cv2.blur(self.image, (7, 7))
        # Erosion d'un mask
        mask=cv2.erode(mask, None, iterations=4)
        # dilatation d'un mask
        mask=cv2.dilate(mask, None, iterations=4)
        self.image2=cv2.bitwise_and(self.frame, self.frame, mask= mask)
        cv2.putText(self.frame, "Couleur: {:d}".format(self.color), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, self.color_info, 1, cv2.LINE_AA)

        # Affichage des composantes HSV sous la souris sur l'image
        pixel_hsv = " ".join(str(values) for values in self.hsv_px)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.frame, "px HSV: "+pixel_hsv, (10, 260),
                font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(elements) > 0:
            #c=max(elements, key=cv2.contourArea)
            for objet in elements:
                ((x, y), rayon)=cv2.minEnclosingCircle(objet)
                if rayon>30:
                    # vue cam overlay
                    cv2.circle(self.image2, (int(x), int(y)), int(rayon), self.color_info, 2)
                    cv2.circle(self.frame, (int(x), int(y)), 5, self.color_info, 10)
                    cv2.line(self.frame, (int(x), int(y)), (int(x)+150, int(y)), self.color_info, 2)
                    cv2.putText(self.frame, "Bouteille !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, self.color_info, 1, cv2.LINE_AA)
                    if self.dist_bout != None :
                        cv2.circle(self.frame, (int(message.x), int(message.y)), 5, self.color_info, 2)
                        cv2.putText(self.frame, "D="+str(round(self.dist_bout,2)), (int(message.x), int(message.y) +30), cv2.FONT_HERSHEY_DUPLEX, 1, self.color_info, 1, cv2.LINE_AA)
            
                    # publish to topic
                    message.x = x
                    message.y = y
                    message.z = 0.0
                    self.publisher_coords_img_bouteille.publish(message)


        cv2.imshow('Camera', self.frame)
        cv2.imshow('image2', self.image2)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(1)&0xFF==ord('q'):
            pass

#########################
#PRINTER AFFICHE RIEN
#########################
    def printer(self, msg):
        self.dist_bout = msg.data



    def process_img(self):
        self.color=70 # HSV : detecter H = 60 (vert vert) pour webcam ; 80 pour realsense

        self.lo=np.array([self.color-40, 100, 50])
        self.hi=np.array([self.color+20, 255,255])

        self.color_info=(0, 0, 255)

        
        cv2.namedWindow('Camera')
        cv2.setMouseCallback('Camera', self.souris)
        self.hsv_px = [0,0,0]

        # Creating morphological kernel
        kernel = np.ones((3, 3), np.uint8)

        print("on va partir dans seuillage")
        self.create_subscription(Image, '/image_image', self.seuillage, 10) 
        self.create_subscription(Float32, '/distance_bouteille', self.printer, 10) 
        self.publisher_coords_img_bouteille = self.create_publisher(Point, '/coords_img_bouteille', 10)
        print("subscribe&publish ok")

        while True: 
            rclpy.spin_once(self, timeout_sec=0.001)
        
        cap.release()
        cv2.destroyAllWindows()



def main():
    print("seuillage")
    rclpy.init()
    minimal_subscriber= Seuillage()
    print("initialisation : ok")
    minimal_subscriber.process_img()

if __name__ == '__main__':
# call main() function
    main()