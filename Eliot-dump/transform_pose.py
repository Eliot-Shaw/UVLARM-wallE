import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import Point, Pose
from visualization_msgs.msg import Marker


def __init__(self):
    tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
    tf_listener = tf2_ros.TransformListener(self.tf_buffer)




def create_bouteille_marker(self):
    bouteille_pose = Pose()
    bouteille_pose.position.x = dx
    bouteille_pose.position.y = dy
    bouteille_pose.position.z = dz
    
    bouteille_pose.orientation.x = 0.0 #sais pas encore
    bouteille_pose.orientation.y = 0.0
    bouteille_pose.orientation.z = 0.0
    bouteille_pose.orientation.w = 0.0

    transform_baselink_map = tf_buffer.lookup_transform("map", "base_link", pose_stamped.header.stamp, rospy.Duration(1.0))
                                                                            #rospy.Time.now()

    self.bouteille_pose_transformed = tf2_geometry_msgs.do_transform_pose(bouteille_pose, transform_baselink_map)
    marker = Marker()
    
    marker.header.frame_id = "map"
    marker.header.stamp = bouteille_pose_transformed.header.stamp

    marker.type = 3 # = cylindre

    # Set the scale of the marker (adjust as needed)
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1

    # Set the color of the marker
    marker.color.a = 1.0  # Alpha (transparency)
    marker.color.r = 1.0  # Red
    marker.color.g = 0.0  # Green
    marker.color.b = 0.0  # Blue

    # Set the pose of the marker based on the transformed pose
    marker.pose = self.bouteille_pose_transformed.pose

    return marker