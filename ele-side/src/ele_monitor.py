#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def ele_location():
    pub = rospy.Publisher('ele_location', String, queue_size=10)
    rospy.init_node('Elevator_monitor', anonymous=False)

    ele_location=1
        #query ele API
    rospy.loginfo("[elevator monitor]now elevator is at:::"+str(ele_location))
    pub.publish(str(ele_location))

    # r = rospy.Rate(1) # 10hz
    # while not rospy.is_shutdown():
    #     ele_location=1
    #     #query ele API

    #     rospy.loginfo("[elevator monitor]now elevator is at:::"+str(ele_location))
    #     pub.publish(str(ele_location))
    #     r.sleep()

if __name__ == '__main__':
    try:
        ele_location()
    except rospy.ROSInterruptException: pass
