#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage  # 改为压缩图像类型
from cv_bridge import CvBridge
import cv2
import numpy as np
from ultralytics import YOLO

class VehicleDetector(Node):
    def __init__(self):
        super().__init__('vehicle_detector')
        # 订阅压缩图像话题（话题名根据 ros2 bag info 的结果修改）
        self.subscription = self.create_subscription(
            CompressedImage,
            '/hikcamera/image_2/compressed',  # 你的实际话题名
            self.image_callback,
            10)
        self.bridge = CvBridge()
        # 加载 YOLOv8 模型（自动下载）
        self.model = YOLO('yolov8n.pt')
        # COCO 数据集中车辆相关类别：car(2), bus(5), truck(7)
        self.vehicle_classes = [2, 5, 7]
        self.get_logger().info('Vehicle detector node started, subscribed to /hikcamera/image_2/compressed')

    def image_callback(self, msg):
        # 将压缩图像解码为 OpenCV 格式
        # 方法1：使用 cv_bridge 的 compressed_imgmsg_to_cv2（需要 cv_bridge 支持）
        # 但 ROS 2 cv_bridge 可能没有直接转换压缩图像的函数，可以用 OpenCV 手动解码
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if cv_image is None:
            self.get_logger().warn('Failed to decode image')
            return

        # 推理
        results = self.model(cv_image, classes=self.vehicle_classes, conf=0.3)
        annotated = results[0].plot()

        # 显示
        cv2.imshow('Vehicle Detection', annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = VehicleDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
