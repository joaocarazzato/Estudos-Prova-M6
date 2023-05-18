import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose as TPose
from time import sleep

MAX_DIFF = 0.1

global posicoesrota 
posicoesrota = [
[5.5, 5.5],
[4.5, 5.5],
[4.5, 4.5],
[5.5, 4.5],
[5.5, 5.5]

]

class Pose(TPose):

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__(x=x, y=y, theta=theta)

    def __repr__(self):
        return f"(x={self.x}, y={self.y})"
    
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __eq__(self, other):
        return abs(self.x - other.x) < MAX_DIFF and abs(self.y - other.y) < MAX_DIFF
    

class TurtleController(Node):
    
    def __init__(self, control_period=0.05):
        super().__init__('turtlecontroller')
        self.x_array = 1
        self.pose = Pose(x = posicoesrota[(self.x_array - 1)][0], y = posicoesrota[(self.x_array - 1)][1])
        self.setpoint = Pose(x = posicoesrota[self.x_array][0], y = posicoesrota[self.x_array][1])
        print(f'self.pose: x={self.pose.x}, y={self.pose.y}')
        print(f'self.setpoint: x={self.setpoint.x}, y={self.setpoint.y}')

        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.control_timer = self.create_timer(timer_period_sec = control_period, callback = self.control_callback)

    def pose_callback(self, msg):
        self.pose = Pose(x=msg.x, y=msg.y, theta=msg.theta)
        if self.setpoint.x == posicoesrota[0][0] and self.setpoint.y == posicoesrota[0][1]:
            self.setpoint = Pose(x=(3.0 + self.pose.x)) # eu nao sei, mas funcionou
        self.get_logger().info(f"A tartaruga está em x={round(msg.x, 2)}, y={round(msg.y, 2)}, theta={round(msg.theta, 2)}")

    def control_callback(self):
        if self.pose.x == posicoesrota[0][0] and self.pose.y == posicoesrota[0][1]:
            self.get_logger().info("Aguardando primeira pose...")
            return 
        msg = Twist()
        self.pose = Pose(x = posicoesrota[(self.x_array - 1)][0], y = posicoesrota[(self.x_array - 1)][1])
        self.setpoint = Pose(x = posicoesrota[self.x_array][0], y = posicoesrota[self.x_array][1])

        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y
        if abs(x_diff) > MAX_DIFF:
            msg.linear.x = 1.0 if x_diff > 0 else -1.0
        if abs(y_diff) > MAX_DIFF:
            msg.linear.y = 1.0 if y_diff > 0 else -1.0
        self.publisher.publish(msg)
        print("self.x_array: ", self.x_array)
        if self.x_array == (len(posicoesrota) - 1):
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            self.get_logger().info("Cheguei no meu destino.")
            exit()
        else:
            self.x_array += 1
        sleep(2)

def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()