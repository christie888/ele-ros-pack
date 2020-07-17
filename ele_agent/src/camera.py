#!/usr/bin/env python

#const std::string cameraImageTopic_ = "/camera/image_raw";
#const std::string cameraInfoTopic_  = "/camera/camera_info";

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError

class camera():
    def __init__(self):
        rospy.init_node('Local_camera', anonymous=False)
        #sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        #self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        self.pub_image = rospy.Publisher("/camera/image_raw",String, queue_size=1)

    def run(self):
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            #str = "hello world %s"%rospy.get_time()
            ele_location="image"
            #query ele API
            self.pub_image.publish(str(ele_location))
            r.sleep()

if __name__ == '__main__':
    try:
        c=camera()
        c.run()
    except rospy.ROSInterruptException: pass