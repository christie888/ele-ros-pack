#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def ele_location():
    pub = rospy.Publisher('ele_location', String, queue_size=10)
    rospy.init_node('ele_location', anonymous=False)
    r = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        #str = "hello world %s"%rospy.get_time()
        ele_location=1
        #query ele API

        rospy.loginfo(ele_location)
        pub.publish(ele_location)
        r.sleep()

if __name__ == '__main__':
    try:
        ele_location()
    except rospy.ROSInterruptException: pass
