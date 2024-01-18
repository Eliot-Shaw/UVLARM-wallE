import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import Point, Pose
from visualization_msgs.msg import Marker


def __init__(self):
    tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
    tf_listener = tf2_ros.TransformListener(self.tf_buffer)



def calcul_distance_bouteille(self, coords_bouteille):
    #Use pixel value of  depth-aligned color image to get 3D axes
    dist = Float32()
    dx ,dy, dz = rs.rs2_deproject_pixel_to_point(self.color_intrin, [int(coords_bouteille.x),int(coords_bouteille.y)], depth)
    dist.data = math.sqrt(((dx)**2) + ((dy)**2) + ((dz)**2))
    print("Distance from camera to pixel:", dist.data)
    if dist.data > 0.15: #éviter les 0 quand le robot va trop vite
        self.publisher_distance_bouteille.publish(dist)
    
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


def create_bouteille_marker(self):
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