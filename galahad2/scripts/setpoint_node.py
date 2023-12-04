#! /usr/bin/env python3

import rclpy
import threading
from rclpy.node import Node 
from std_msgs.msg import Float32

angle = Float32()

class SetpointNode(Node):
    
    def __init__(self): 
        super().__init__('setpoint_node')
        
        self.setpoint_pub = self.create_publisher(Float32, '/setpoint/angle', 10)

def main():
    angle.data = 1.5
    node.setpoint_pub.publish(angle)

if __name__ == '__main__':
    rclpy.init()

    node = SetpointNode()

    thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
    thread.start()

    rate = node.create_rate(10)
    
    try: 
        while rclpy.ok(): 
            main()
            rate.sleep()
        
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
    thread.join()
