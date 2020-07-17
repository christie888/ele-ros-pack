#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
#from ar_pose import ARMarker
from ar_pose.msg import ARMarker

class Agent():
    def __init__(self):
        self.process_id=0
        self.auth=False
        self.robot_departure=None
        self.robot_destination=None
        self.poseFlag=False
        self.robot_movingtime=0
        self.elevator_movingtime=0
        self.eleLocation=None

        self.pub_processid=rospy.Publisher("Process_id",Int16,queue_size=1)
        
        self.pub_error=rospy.Publisher("Error",String,queue_size=1)
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        self.pub_robot_movingtime =rospy.Publisher("moving_time",Int16,queue_size=1)
        #rospy.init_node('Process', anonymous=False)
        #rospy.Subscriber("/camera_prefix/image_rect", Image, self.chek_authority)
        rospy.Subscriber("/robot_departure",Int16, self.callback_departureFloor)
        rospy.Subscriber("/robot_destination",Int16, self.callback_destinationFloor)
        rospy.Subscriber("Error", String, self.callback_error)
        rospy.Subscriber("/ele_location",String, self.callback_eleLocation)
        #rospy.Subscriber("/camera/image_raw",String, self.callback_image_raw)
        rospy.Subscriber("/ar_pose_marker",ARMarker, self.callback_arpose)

       

    def callback_arpose(self,data):
        pass

    def callback_image_raw(self,data):
        pass
    def callback_error(self,data):
        self.error=data.data

    def callback_destinationFloor(self,value):
        self.robot_destination=value.data
        rospy.loginfo("destination floor is ::: "+str(self.robot_destination))

    def callback_departureFloor(self,floorValue):
        self.robot_departure=floorValue
        rospy.loginfo("departure floor is ::: "+str(self.robot_departure))

    def chek_authority(self):#chek_authority(self,img):
        #check authority by img
        self.auth=True #else publish error
        rospy.loginfo("authorized ::: ok")               
        self.process_id=self.process_id+1
    
    def NavigateRobot(self):
        #rospy.init_node('NavigateRobot', anonymous=False)
        data = Twist()
        data.linear.x = 0.0#calculate linear 
        data.angular.z = 1#calculate angular
        time=3 #calculate time
        self.cmd_vel.publish(data)
        self.pub_robot_movingtime.publish(time)

    def callback_eleLocation(self,eleLocation):
        self.eleLocation=eleLocation.data
        rospy.loginfo("[egent process] elevator location is::::"+str(self.eleLocation))
    
    def checkPose(self):
        #rospy.init_node('CheckPose', anonymous=False)
        self.poseFlag=True
        self.robot_movingtime=10
        self.process_id=self.process_id+1
          
    def monitoring_elevator(self,floor):
        #rospy.init_node('MonitorElevator', anonymous=False)
        rospy.loginfo("monitoring elevator :::") 
        r = rospy.Rate(1) # 10hz
        elevator_now=-2
        while not rospy.is_shutdown() and elevator_now!=floor:
            #get elevator postion
            rospy.loginfo("now elevator is at :::"+str(elevator_now)) 
            elevator_now=elevator_now+1
            r.sleep()
        
        rospy.loginfo(" elevator arrived at :::"+str(floor)) 
        self.process_id=self.process_id+1

    def pubProcessId(self,duration):
        r = rospy.Rate(1)
        now=rospy.Time.now().to_sec()
        end=rospy.Time.now().to_sec()+duration
        rospy.loginfo("current time:::"+str(now)+"duration:::"+str(duration)+"end time:::"+str(end))

        while not rospy.is_shutdown() and rospy.Time.now().to_sec()<end:
            self.pub_processid.publish(self.process_id)
            rospy.loginfo("current time of seconds:::"+str(rospy.Time.now().to_sec()))
            r.sleep()


    def callElevator(self, floorNum):
        #rospy.init_node('CallElevator', anonymous=False)
        self.pub_ele_dest=rospy.Publisher("destination",String,queue_size=1)
        self.pub_ele_dest.publish(floorNum)
        rospy.loginfo("call elevator to floor:::"+str(floorNum))
        #elevator API

    def Error(self):
        rospy.loginfo("Error:::")
        self.pub_error.publish(self.process_id)
    
        
    def run(self):
        self.chek_authority()
        self.callback_departureFloor(1)
        #r = rospy.Rate(1)
        #while not rospy.is_shutdown():
        
        self.pubProcessId(3)
        self.checkPose()
        #print(self.robot_movingtime)
        #rospy.loginfo("robot moving time:::"+str(self.robot_movingtime))
        rospy.sleep(float(self.robot_movingtime))

        self.NavigateRobot()#check pose standby
        rospy.sleep(float(self.robot_movingtime))
        
        self.pubProcessId(5)

        if self.robot_departure !=None:
            self.callElevator(self.robot_departure)
            #self.monitoring_elevator(self.robot_departure)
        else:
            self.Error()

        #self.pubProcessId()
        self.NavigateRobot()#navigate to ride on
        rospy.sleep(float(self.robot_movingtime))

        #self.pubProcessId()
        #self.callElevator(self.robot_destination)
        if self.robot_destination!=None:
            self.robot_destination=3
            self.callElevator(self.robot_destination)
            self.monitoring_elevator(self.robot_destination)
        else:
            self.Error()
        #self.pubProcessId()

        #r.sleep()
        #if self.auth==True and self.departureFloor!=None:
    
if __name__ == '__main__':
    #devfile = '/dev/triggerSensor'
    #http://wiki.ros.org/visp_tracker#Subscribed_Topics visp tracker
    #sub = rospy.Subscriber("/camera_prefix/image_rect", Image, self.get_image)
    #robot_departure_floor=2
    rospy.init_node('Agent_Process', anonymous=False)
    agent=Agent()
    agent.run()

    #rospy.wait_for_service('/trigger_on')
   