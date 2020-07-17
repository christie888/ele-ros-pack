#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
#from robot_side.srv import TimedMotion

class Robot():
    def __init__(self):
        self.process_id=0
        self.linear=0
        self.angular=0
        self.move_time=0
        self.error=None
        self.destination=None
        self.last_time = None#rospy.Time.now()
        rospy.init_node('Robot', anonymous=False)
        #rospy.loginfo("received process id is ::: %f",self.process_id)
        rospy.Subscriber("Process_id", Int16, self.callback_process_id)
        rospy.Subscriber("Error", String, self.callback_error)
        self.pub_destination=rospy.Publisher("robot_destination",Int16,queue_size=1)
        rospy.Subscriber("moving_time", Int16, self.callback_movingtime)
        rospy.Subscriber('/cmd_vel', Twist, self.callback_cmd_vel)
        self.pub_error=rospy.Publisher("Error",String,queue_size=1)

        rospy.spin()
        #rospy.spin()

    def callback_error(self,data):
        self.error=data.data
        #processError

    def callback_process_id(self,data):
        self.process_id=data.data
        rospy.loginfo("process id is ::: %s",self.process_id)
    
    def processing(self):
        #rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            if self.process_id==1:#change pose
                rospy.loginfo("change pose")
                #change_pose
                self.last_time = rospy.Time.now()
                self.move()
                #rospy.sleep(self.move_time)
            elif self.process_id ==2:#call elevator
                rospy.loginfo("call elevator")
                r = rospy.Rate(1)
                i=0
                while not rospy.is_shutdown() and i<=3:
                    self.pub_destination.publish(self.destination)
                    rospy.loginfo("destination is %f",self.destination)
                    i=i+1
                    r.sleep()

            elif self.process_id ==3:#move to ride on
                rospy.loginfo("move to ride on")
                #change_pose
                #rospy.Subscriber("Moving_time", Int16, self.callback_movingtime)
                #rospy.Subscriber('cmd_vel', Twist, self.callback_cmd_vel)
                self.last_time = rospy.Time.now()
                self.move()
                #rospy.sleep(float(self.move_time))
    
    def callback_movingtime(self,message):
        self.move_time=message.data
        rospy.loginfo("moving time is ::: %s",self.move_time)
       

    def callback_cmd_vel(self,message):
        self.linear =  message.linear.x #80000.0*message.linear.x/(9*math.pi)
        self.angular = message.angular.z#400.0*message.angular.z/math.pi
        #self.set_raw_freq(forward_hz-rot_hz, forward_hz+rot_hz)
        rospy.loginfo("cmd verocity is :::"+str(message))

    def move(self):
        r = rospy.Rate(1)
        duration=self.move_time
        now=rospy.Time.now().to_sec()
        end=rospy.Time.now().to_sec()+duration
       
        while not rospy.is_shutdown() and rospy.Time.now().to_sec()<end:
            rospy.loginfo("robot is moving:::"+str(rospy.Time.now().to_sec()))
            ##Moving with the cmd vel
            r.sleep()

if __name__ == '__main__':
    r=Robot()
    r.destination=3
    r.processing()
