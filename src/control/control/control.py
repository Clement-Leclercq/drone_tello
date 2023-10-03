import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from std_msgs.msg import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from time import sleep

class Control(Node):

    def __init__(self):
        super().__init__('control')
        self.subscription_controller = self.create_subscription(
            Joy,
            'joy',
            self.controller_callback,
            10)

        self.subscription_takeoff = self.create_subscription(
            Empty,
            'takeoff',
            self.takeoff_callback,
            10)

        self.subscription_land = self.create_subscription(
            Empty,
            'land',
            self.land_callback,
            10)

        self.subscription_controller  # prevent unused variable warning
        self.subscription_takeoff   # prevent unused variable warning
        self.subscription_land  # prevent unused variable warning
    
        self.data_joy = []
        self.joy_left = [0.0, 0.0]
        self.joy_right = [0.0, 0.0]

        self.fly = False
        self.publisher_land = self.create_publisher(Empty,'land',10)
        self.publisher_takeoff = self.create_publisher(Empty,'takeoff',10)
        self.publisher_emergency = self.create_publisher(Empty,'emergency',10)
        self.publisher_flip = self.create_publisher(String,'flip',10)
        self.publisher_control = self.create_publisher(Twist,'control',10)


    def takeoff_callback(self,msg):
        self.fly = True
        self.get_logger().info('Flying Status: TRUE')

    def land_callback(self,msg):
        self.fly = False
        self.get_logger().info('Flying Status: FALSE')

    def controller_callback(self, msg):

        self.joy_left = msg.axes[:2]
        self.joy_right = msg.axes[3:5]

        self.data_joy = msg.buttons
        if self.data_joy[8] == 1:
            self.get_logger().info('EMERGENCY !!!')
            send = Empty()
            self.publisher_emergency.publish(send)

        if not self.fly and self.data_joy[7] == 1: 
            self.fly = True
            self.get_logger().info('Taking off !!!')
            send = Empty()
            self.publisher_takeoff.publish(send)    

        elif self.fly and self.data_joy[6] == 1:
            self.fly = False
            self.get_logger().info('Landing !!!')
            send = Empty()
            self.publisher_land.publish(send)

        elif self.fly and self.data_joy[0] == 1:
            self.get_logger().info('BACKFLIP !!!')
            send = String()
            send.data = 'b'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[1] == 1:
            self.get_logger().info('RIGHTFLIP !!!')
            send = String()
            send.data = 'r'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[2] == 1:
            self.get_logger().info('LEFTFLIP !!!')
            send = String()
            send.data = 'l'
            self.publisher_flip.publish(send)
            sleep(0.4)

        elif self.fly and self.data_joy[3] == 1:
            self.get_logger().info('FRONTFLIP !!!')
            send = String()
            send.data = 'f'
            self.publisher_flip.publish(send)
            sleep(0.4)

        if self.fly:
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
