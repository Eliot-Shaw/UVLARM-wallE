# Realsense Node:
class Realsense(Node):
    def __init__(self, fps= 60):
        super().__init__('realsense')

    def read_imgs(self):
        pass

    def publish_imgs(self):
        pass

    def process_img(args=None):
        rclpy.init(args=args)
        rsNode= Realsense()
        while isOk:
            rsNode.read_imgs()
            rsNode.publish_imgs()
            rclpy.spin_once(rsNode, timeout_sec=0.001)
        # Stop streaming
        print("Ending...")
        rsNode.pipeline.stop()
        # Clean end
        rsNode.destroy_node()
        rclpy.shutdown()