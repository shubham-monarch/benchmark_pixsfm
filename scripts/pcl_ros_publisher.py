import rospy
import pcl
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from pcl import pcl_conversions

def publish_point_cloud(ply_file, publisher):
    # Load .ply file
    cloud = pcl.load(ply_file)

    # Convert to ROS message
    cloud_msg = pcl_conversions.pcl_to_ros(cloud)

    # Publish the data
    publisher.publish(cloud_msg)

def main():
    # Initialize ROS node
    rospy.init_node('point_cloud_publisher')

    # Create publishers
    pub1 = rospy.Publisher('point_cloud1', PointCloud2, queue_size=10)
    pub2 = rospy.Publisher('point_cloud2', PointCloud2, queue_size=10)

    # Path to your .ply files
    ply_file1 = "/path/to/your/first.ply"
    ply_file2 = "/path/to/your/second.ply"

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # Publish point clouds
        publish_point_cloud(ply_file1, pub1)
        publish_point_cloud(ply_file2, pub2)

        rate.sleep()

if __name__ == '__main__':
    print("Inside the main funtion!")
    main()