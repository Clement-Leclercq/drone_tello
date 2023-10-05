#Import de l'ensemble des modules ROS et interfaces qu'on utilise dans l'ensemble du code
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from std_msgs.msg import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from time import sleep

#Création de la classe Control qui sera notre Node Control
class Control(Node):

    def __init__(self):
        super().__init__('control')
        #Création d'un subsciber au topic joy permettant d'écouter les messages
        #de type Joy, utilisé ici pour écouter la manette
        self.subscription_controller = self.create_subscription(
            Joy,
            'joy',
            self.controller_callback,
            10)
        
        #Création d'un subsciber au topic takeoff permettant d'écouter les messages
        #de type Empty, utilisé ici pour savoir si le drone a décollé ou non depuis
        #un appel extérieur à cette node
        self.subscription_takeoff = self.create_subscription(
            Empty,
            'takeoff',
            self.takeoff_callback,
            10)
        
        #Création d'un subsciber au topic land permettant d'écouter les messages
        #de type Empty, utilisé ici pour savoir si le drone a atteri ou non depuis
        #un appel extérieur à cette node
        self.subscription_land = self.create_subscription(
            Empty,
            'land',
            self.land_callback,
            10)

        self.subscription_controller  # prevent unused variable warning
        self.subscription_takeoff   # prevent unused variable warning
        self.subscription_land  # prevent unused variable warning

        #Initialisation de quelques variables de stockage utile dans certaines callback
        self.data_joy = []
        self.joy_left = [0.0, 0.0]
        self.joy_right = [0.0, 0.0]
        self.fly = False

        #Initialisation de l'ensemble de nos publisher
        self.publisher_land = self.create_publisher(Empty,'land',10)
        self.publisher_takeoff = self.create_publisher(Empty,'takeoff',10)
        self.publisher_emergency = self.create_publisher(Empty,'emergency',10)
        self.publisher_flip = self.create_publisher(String,'flip',10)
        self.publisher_control = self.create_publisher(Twist,'control',10)

    def takeoff_callback(self,msg):
        # Callback de notre subscriber de takeoff, à chaque fois qu'un message est envoyé sur le topic takeoff
        # on considère que le drone est en vol et on met à jour self.fly à TRUE
        self.fly = True
        self.get_logger().info('Flying Status: TRUE')

    def land_callback(self,msg):
        # Callback de notre subscriber de land, à chaque fois qu'un message est envoyé sur le topic land
        # on considère que le drone n'est plus en vol et on met à jour self.fly à FALSE
        self.fly = False
        self.get_logger().info('Flying Status: FALSE')

    def controller_callback(self, msg):
        # Callback de notre subscriber de joy, à chaque fois que l'on envoit des commandes avec la manette xbox
        # nous récupérons ici les données importantes et nous envoyons les différentes commandes de contrôle à 
        # notre drone
        self.joy_left = msg.axes[:2]
        self.joy_right = msg.axes[3:5]

        self.data_joy = msg.buttons
        if self.data_joy[8] == 1:
            #Bouton central permettant d'effectuer un arrêt d'urgence du drone
            self.get_logger().info('EMERGENCY !!!')
            send = Empty()
            self.publisher_emergency.publish(send)

        if not self.fly and self.data_joy[7] == 1: 
            #Bouton central droit permettant d'effectuer un décollage (uniquement si le drone n'est pas en vol)
            self.fly = True
            self.get_logger().info('Taking off !!!')
            send = Empty()
            self.publisher_takeoff.publish(send)    

        elif self.fly and self.data_joy[6] == 1:
            #Bouton central gauche permettant d'effectuer un atterissage (uniquement si le drone est en vol)
            self.fly = False
            self.get_logger().info('Landing !!!')
            send = Empty()
            self.publisher_land.publish(send)

        elif self.fly and self.data_joy[0] == 1:
            # Bouton ABXY permettant d'effectuer un backflip
            self.get_logger().info('BACKFLIP !!!')
            send = String()
            send.data = 'b'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[1] == 1:
            # Bouton ABXY permettant d'effectuer un flip sur la droite
            self.get_logger().info('RIGHTFLIP !!!')
            send = String()
            send.data = 'r'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[2] == 1:
            # Bouton ABXY permettant d'effectuer un flip sur la gauche
            self.get_logger().info('LEFTFLIP !!!')
            send = String()
            send.data = 'l'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[3] == 1:
            # Bouton ABXY permettant d'effectuer un frontflip
            self.get_logger().info('FRONTFLIP !!!')
            send = String()
            send.data = 'f'
            self.publisher_flip.publish(send)
            sleep(0.4)

        if self.fly:
            # Gestion de la valeur des Joysticks pour contrôler le drone
            # Joystick gauche gère l'altitude (joystick bas / haut) et la rotation (joystick gauche / droite)
            # Joystick droit gère le déplacement avant / arrière et gauche / droite du drone
            facteur = 100
            commande = Twist()
            commande.linear.x = self.joy_right[0]*(-1.0)*facteur
            commande.linear.y = self.joy_right[1]*facteur
            commande.linear.z = self.joy_left[1]*facteur
            commande.angular.x = 0.0
            commande.angular.y = 0.0
            commande.angular.z = self.joy_left[0]*(-1.0)*facteur
            self.publisher_control.publish(commande)
        

def main():
    #Création de la node et de la boucle rclpy
    rclpy.init()
    control = Control()
    rclpy.spin(control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
