import tf2_ros
import tf2_geometry_msgs

def __init__(self):
    tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
    tf_listener = tf2_ros.TransformListener(self.tf_buffer)

def transformation(self):
    transform = tf_buffer.lookup_transform(target_frame,
                                       # source frame:
                                       pose_stamped.header.frame_id,
                                       # get the tf at the time the pose was valid
                                       pose_stamped.header.stamp,
                                       # wait for at most 1 second for transform, otherwise throw
                                       rospy.Duration(1.0))

    pose_transformed = tf2_geometry_msgs.do_transform_pose(pose_stamped, transform)