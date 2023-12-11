#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32MultiArray 
from scipy.spatial.transform import Rotation

def callback(data):
   #pose
   x=data.pose.position.x
   y=data.pose.position.y
   z=data.pose.position.z
   
   #orientation
   ori_x=data.pose.orientation.x
   ori_y=data.pose.orientation.y
   ori_z=data.pose.orientation.z
   ori_w=data.pose.orientation.w
   
   
   rotation = Rotation.from_quat([ori_x, ori_y, ori_z, ori_w])
   euler_angles = rotation.as_euler('xyz', degrees=True)
   
   #orientation adjust 0-360
   yaw = euler_angles[2] + 360 if euler_angles[2] < 0 else euler_angles[2]

   position=Int32MultiArray(data=[int(x*10000),int(y*10000),int(z*10000),int(yaw*100),int(euler_angles[0]*100),int(euler_angles[1]*100)])
   print(position)
   pub.publish(position)

def sendPos():
   global pub
   rospy.init_node('DronePose',anonymous=False)
   pub = rospy.Publisher('Pose', Int32MultiArray, queue_size=10)
   rospy.Subscriber("/mavros/local_position/pose",PoseStamped, callback)
   rospy.spin()

if __name__ == '__main__':
    sendPos()
