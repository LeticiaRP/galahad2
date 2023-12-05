#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import cv2 as cv 

TOLERANCIA = 100

# modificar para um ajuste (25, 100, 102)  (21, 45, 102)
verdeClaro = (25, 100, 102)
verdeEscuro = (70, 255, 255)


def bola(frame):

    # aplica mascara das cores
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, verdeClaro, verdeEscuro)
    # filtra a imagem
    mascE = cv.erode(mask, None, iterations=2)
    mascD = cv.dilate(mascE, None, iterations=2)

   # acha os contornos
    cnts = cv.findContours(mascD.copy(), cv.RETR_EXTERNAL,
                           cv.CHAIN_APPROX_SIMPLE)[-2]
    # se tiver achado alguma coisa
    if len(cnts) > 0:

        c = max(cnts, key=cv.contourArea)
        for i in cnts:
            ((x, y), radius) = cv.minEnclosingCircle(c)

            if (radius < 300) & (radius > 10):

                cv.circle(frame, (int(x), int(y)), int(
                    radius), (255, 255, 255), 2)

                # X
                cv.line(frame, (int(x), 0), (int(x), 500),
                        (255, 255, 255), thickness=1)
                # Y
                cv.line(frame, (0, int(y)), (700, int(y)),
                        (255, 255, 255), thickness=1)

                cv.putText(frame, "X: " + str(int(x))+" Y: "+str(int(y)), (50, 375),
                           cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), thickness=1)
                cord = (int(x), int(y))

                return frame, cord
    return frame, None


class CameraPublisher(Node):
    def __init__(self):
        super().__init__('id_target')
        self.publisher = self.create_publisher(Image, 'camera/detection', 10)
        self.subscription = self.create_subscription(
            Image,
            'camera/raw',
            self.callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

                # aplica mascara das cores
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, verdeClaro, verdeEscuro)
        # filtra a imagem
        mascE = cv.erode(mask, None, iterations=2)
        mascD = cv.dilate(mascE, None, iterations=2)

        # acha os contornos
        cnts = cv.findContours(mascD.copy(), cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)[-2]
        # se tiver achado alguma coisa
        if len(cnts) > 0:

            c = max(cnts, key=cv.contourArea)
            for i in cnts:
                ((x, y), radius) = cv.minEnclosingCircle(c)

                if (radius < 300) & (radius > 10):

                    cv.circle(frame, (int(x), int(y)), int(
                        radius), (255, 255, 255), 2)

                    # X
                    cv.line(frame, (int(x), 0), (int(x), 500),
                            (255, 255, 255), thickness=1)
                    # Y
                    cv.line(frame, (0, int(y)), (700, int(y)),
                            (255, 255, 255), thickness=1)

                    cv.putText(frame, "X: " + str(int(x))+" Y: "+str(int(y)), (50, 375),
                                cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), thickness=1)
                    cord = (int(x), int(y))


        # Draw a number on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = '42'
        position = (50, 50)
        color = (255, 255, 255)
        thickness = 2
        cv2.putText(frame, text, position, font, 1, color, thickness, cv2.LINE_AA)

        # Convert the image back to ROS Image message
        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')

        # Publish the modified image
        self.publisher.publish(img_msg)
        self.get_logger().info('Image with number published')

def main(args=None):
    rclpy.init(args=args)

    camera_publisher = CameraPublisher()

    rclpy.spin(camera_publisher)

    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
