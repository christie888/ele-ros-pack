#!/usr/bin/env python

import rospy
from std_msgs.msg import String


class Ele_control():
    def __init__(self):
    	self.destination=None
    	rospy.loginfo("started node of ele_control -----")
    	rospy.init_node('Elevator_control', anonymous=False)
    	rospy.Subscriber('destination', String, self.callback_destination)
   
    	rospy.spin()


    def callback_destination(self, message):
    	self.destination=message.data
    	if self.destination!=None:
    	#api call elevator
           rospy.loginfo("call elevator to te deatination of -----",str(self.destination))

if __name__ == '__main__':
    try:
        Ele_control()
    except rospy.ROSInterruptException: pass
