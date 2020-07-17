#!/usr/bin/env python

import rospy
from std_msgs.msg import String


class Robot_process():
            
    def call_back(data):
        self.process_id=data.data
        rospy.loginfo("my process id is ::: %f",self.process_id)

    def __init__(self):
        self.process_id=0
        prcess_sub=rospy.Subscriber("Process_id", String, self.callback)



if __name__ == '__main__':
    rospy.init_node('Robot', anonymous=False)
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            Robot_process()
            r.sleep()
        except rospy.ROSInterruptException: pass
