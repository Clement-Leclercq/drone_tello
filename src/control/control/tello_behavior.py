#Import de l'ensemble des modules ROS et interfaces qu'on utilise dans l'ensemble du code
import sys
import rclpy
from rclpy.node import Node
from time import sleep

import time
import cv2
import numpy as np
import sklearn
from cv_bridge import CvBridge 


from control_interfaces.srv import DroneMode
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import Image


class Behavior(Node):

    def __init__(self):
        super().__init__('Behavior')

        # self.subscription_joy = self.create_subscription(
        #     Joy,
        #     'joy',
        #     self.joy_callback,
        #     10)
        # self.subscription_joy  # prevent unused variable warning

        
        # Création du subscriber au topic secure_cmd pour écouter la node control
        self.subscription_manual = self.create_subscription(
            Twist,
            'secure_cmd',
            self.manual_mode,
            10)
        self.subscription_manual # prevent unused variable warning

        # Création du subscriber au topic image_raw qui nous permet de récupérer les infos caméras du drone
        self.subscription_qr = self.create_subscription(
            Image,
            'image_raw',
            self.qr_mode,
            10)
        self.subscription_qr # prevent unused variable warning


        # Création du serveur du service drone_mode
        self.srv = self.create_service(DroneMode, 'drone_mode', self.drone_mode_callback)

        # Création de nos publishers
        self.publisher_control = self.create_publisher(Twist,'control',10)

        #Variable globale
        self.mode = None

        # Création du client du service drone_mode 
        self.drone_mode_client = self.create_client(DroneMode, 'drone_mode')
        while not self.drone_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("CLIENT: Drone_mode Service not available, waiting again...")
        # Envoi d'une requete de mode de vol manuel pendant l'initialisation de la node ce qui
        # nous permet de contrôler manuellement le drone
        self.req = DroneMode.Request()
        response = self.send_request(0)
        self.get_logger().info('CLIENT: Changing mode : %d' % (response.status))

        # Création d'une clock de 1 seconde qui appelle la callback scout_mode
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.scout_mode)

        # Mise en place de variable permettant le traitement des images avec opencv 
        self.br = CvBridge()

        self.errList = [0,0] #x,z
        self.errListFollow = [0,0,0] #x,y,z

        self.actionList = [0,0]
        # Attention à bien modifier le path menant à la cascade de haar
        self.body_cascade = cv2.CascadeClassifier('/home/triton_10/ros2_ws_lp/haarcascade_frontalface_default.xml')





    def send_request(self, mode):
        # Partie client avec call asynchrone permettant de changer de mode
        # Il est impossible de lancer cette callback depuis une autre callback
        # Il nous a donc été impossible de mapper le changement de mode avec la manette
        # Pour changer de mode il faut faire un appel terminal


        self.req.mode = mode
        self.get_logger().info('CLIENT: Sending Request...')
        self.future = self.drone_mode_client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        self.get_logger().info('CLIENT: Request Sent...')
        return self.future.result()

    # def joy_callback(self,msg):
    #     self.get_logger().info('llal')
    #     if msg.axes[7] == 1.0 :
    #         self.get_logger().info('CLIENT: Changing mode : Manual')
    #         self.flag_cmd[0] = True
    #         # while not self.drone_mode_client.wait_for_service(timeout_sec=1.0):
    #         #     self.get_logger().info("CLIENT: Drone_mode Service not available, waiting again...")
    #         # response = self.send_request(0)
    #         # self.get_logger().info('CLIENT: Changing mode : %d' % (response.status))
    #     elif msg.axes[6] == -1.0:
    #         self.get_logger().info('CLIENT: Changing mode : Scout')
    #         self.flag_cmd[1] = True
    #         # while not self.drone_mode_client.wait_for_service(timeout_sec=1.0):
    #         #     self.get_logger().info("CLIENT: Drone_mode Service not available, waiting again...")
    #         # response = self.send_request(1)
    #         # self.get_logger().info('CLIENT: Changing mode : %d' % (response.status))
    #     elif msg.axes[2] == -1.0:
    #         self.get_logger().info('CLIENT: hanging mode : Spielberg')
    #         self.flag_cmd[2] = True
    #         # while not self.drone_mode_client.wait_for_service(timeout_sec=1.0):
    #         #     self.get_logger().info("CLIENT: Drone_mode Service not available, waiting again...")
    #         # response = self.send_request(2)
    #         self.get_logger().info('CLIENT: Changing mode : %d' % (response.status))
    #     elif msg.axes[3] == 1.0:
    #         self.get_logger().info('CLIENT: Changing mode : QR Code')
    #         self.flag_cmd[3] = True
    #         # while not self.drone_mode_client.wait_for_service(timeout_sec=1.0):
    #         #     self.get_logger().info("CLIENT: Drone_mode Service not available, waiting again...")
    #         # response = self.send_request(3)
    #         # self.get_logger().info('CLIENT: Changing mode : %d' % (response.status))
        


    def drone_mode_callback(self, request, response):
        # Partie Serveur du service drone_mode
        
        commande = Twist()
        commande.linear.x = 0.0
        commande.linear.y = 0.0
        commande.linear.z = 0.0
        commande.angular.x = 0.0
        commande.angular.y = 0.0
        commande.angular.z = 0.0
        self.publisher_control.publish(commande)


        response.status = False
        self.get_logger().info('SERVER: Incoming request %d '% (request.mode))
        self.mode = request.mode
        match self.mode:
            case 0:
                #mode manuel
                #le drone se pilote via la manette
                self.get_logger().info("SERVER: Setting Manual Mode")
                response.status = True

            case 1:
                #mode surveillance
                #le drone tourne sur lui même sur une position stationnaire
                self.get_logger().info("SERVER: Setting Scout Mode")
                response.status = True
            case 2: 
                #mode Spielberg
                #le drone suit la personne qu'il reconnait
                self.get_logger().info("SERVER: Setting Spielberg Mode")
                response.status = True
            case 3:
                #mode follower de QR Code
                #le drone se centre sur le qr code qu'on lui présente
                self.get_logger().info("SERVER: Setting qr Mode")
                response.status = True
        return response


    def manual_mode(self, msg):
        if self.mode == 0:
            #Si nous sommes bien en mode manuel, nous laissons simplement passé les messages arrivant sur le topic /secure_cmd
            #pour les publier sur le topic /control
            self.publisher_control.publish(msg)

    def scout_mode(self):
        if self.mode == 1 :
            #Envoi de la commande de controle permettant la rotation du drone sur lui même en mode scout
            commande = Twist()
            commande.linear.x = 0.0
            commande.linear.y = 0.0
            commande.linear.z = 0.0
            commande.angular.x = 0.0
            commande.angular.y = 0.0
            commande.angular.z = 20.0
            self.publisher_control.publish(commande)
    
    def qr_mode(self,msg):
        if self.mode == 3:
            #Fonction permettant de centrer le drone sur un QR code qu'il détecte (n'importe quel QR Code)
            frame = self.br.imgmsg_to_cv2(msg)

            
            qr_decoder = cv2.QRCodeDetector()
            # Detect and decode the qrcode
            data, bbox, rectified_image = qr_decoder.detectAndDecode(frame)
            if len(data)>0:
                pt1 = int(bbox[0][0][0]), int(bbox[0][0][1])    # angle en haut à gauche
                pt2 = int(bbox[0][2][0]), int(bbox[0][2][1])    # angle en bas à droite
                ptCentre = int(bbox[0][0][0]) + int((pt2[0] - pt1[0])/2) , int(bbox[0][0][1]) + int((pt2[1] - pt1[1])/2)

                img_center = (int(msg.width/2),int(msg.height/2))

                commande = Twist()
        
                delta = (ptCentre[0] - img_center[0],ptCentre[1] - img_center[1])

                errx = delta[0]
                erry = delta[1]


                self.get_logger().info("CENTRE X: %f" % ptCentre[0])
                self.get_logger().info("CENTRE Y: %f" % ptCentre[1])

                self.get_logger().info("IMAGE CENTRE X: %f" % img_center[0])
                self.get_logger().info("IMAGE CENTRE Y: %f" % img_center[1])

                self.get_logger().info("DELTA X: %f" % delta[0])
                self.get_logger().info("DELTA Y: %f" % delta[1])



                # commande.linear.x = (delta[0] * 25 * 2)/(img_center[0])
                # commande.linear.z = -1*(delta[1] * 25 * 2)/(img_center[1])
                

                if abs(errx) > 100  or abs(erry) > 50 : 
                    commande.linear.x = (self._pid(errx,self.errList[0], 10 , 0.2, 5)* 2 )/(img_center[0])
                    commande.linear.z = -1*(self._pid(erry,self.errList[1], 15 , 0.8 , 5)* 2 )/(img_center[1])
                else :
                    commande.angular.x = 0.0           
                    commande.angular.z = 0.0
                

                
                self.actionList[0] = commande.linear.x
                self.actionList[1] = commande.linear.z
                self.errList = delta


                self.get_logger().info("LINEAR X: %f" % commande.linear.x)
                self.get_logger().info("LINEAR Z: %f" % commande.linear.z)

                commande.linear.y = 0.0
                commande.angular.x = 0.0
                commande.angular.y = 0.0
                commande.angular.z = 0.0
                self.publisher_control.publish(commande)
            else:
                #Si nous ne détectons pas de QR code, nous ordonnons au drone de ne pas bouger
                commande = Twist()
                commande.linear.x = 0.0
                commande.linear.y = 0.0
                commande.linear.z = 0.0
                commande.angular.x = 0.0
                commande.angular.y = 0.0
                commande.angular.z = 0.0
                self.publisher_control.publish(commande)

        if self.mode == 2:   
            # Partie en mode SPIELBERG qui nous permet de suivre une personne après une détection de visage via un cascade de HAAR
            frame = self.br.imgmsg_to_cv2(msg)
            # Convert the image to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces in the image
            body = self.body_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            commande = Twist()
            img_center = (int(msg.width/2),int(msg.height/2))


            if len(body) != 0 :
                (x,z,w,h) = body[0]
                faceWidth = 80
    
                ptCentre = [int(x + w/2),int(z + h/2)]

                deltaY = w - faceWidth 
                delta = (ptCentre[0] - img_center[0],ptCentre[1] - img_center[1])

                errx = delta[0]
                erry = delta[1]   


                commande.linear.x = (self._pid(errx,self.errListFollow[0], 25 , 0.2, 5)* 2 )/(img_center[0])
                commande.linear.z = -1*(self._pid(erry,self.errListFollow[2], 10 , 0.2, 5)* 2 )/(img_center[1])
                commande.linear.y = -1*(self._pid(deltaY,self.errListFollow[1], 50 , 10, 10))/(faceWidth)


                commande.angular.x = 0.0
                commande.angular.y = 0.0
                commande.angular.z = 0.0


                self.errListFollow[0] = delta[0]
                self.errListFollow[1] = deltaY
                self.errListFollow[2] = delta[1]

                self.get_logger().info("LINEAR X: %f" % commande.linear.x)
                self.get_logger().info("LINEAR Y: %f" % commande.linear.y)
                self.get_logger().info("LINEAR Z: %f" % commande.linear.z)

                self.publisher_control.publish(commande)

            else:
                commande.linear.x = 0.0
                commande.linear.y = 0.0
                commande.linear.z = 0.0
                commande.angular.x = 0.0
                commande.angular.y = 0.0
                commande.angular.z = 0.0
                self.publisher_control.publish(commande)
                
    def _pid(self, err, err_1, Kp, Ki, Kd):
        # Fonction PID basique permettant d'éviter les trops fortes oscillations en mode Follower de QR Code et en mode Spielberg
        return Kp*err + Ki*(err+err_1) + Kd*(err-err_1) 

            

    
def main():
    rclpy.init()
    behavior = Behavior()
    rclpy.spin(behavior)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    behavior.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
