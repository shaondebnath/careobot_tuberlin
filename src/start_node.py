#!/usr/bin/python

import rospy

from simple_script_server import script

import tf
from geometry_msgs.msg import *
from moveit_msgs.srv import *

from move_arm import *
from mygrasps_node import *

class MyScript(script):
    def Initialize(self):
        # Initialize the component
        rospy.loginfo("Initializing all components...")
        
        components_to_init = ['tray', 'torso', 'arm', 'base', "gripper"]
        
        for component in components_to_init:
            self.sss.init(component)
                    
        
        self.istener = tf.TransformListener(True, rospy.Duration(10.0))
        
        self.sss.move("torso","home",False)
        self.sss.move("tray","down",False)
        handle_arm = self.sss.move("arm","folded")
        handle_gripper = self.sss.move("gripper","home", False) #true
        
        handle_arm.wait()
        handle_gripper.wait()
        

    def Run(self):
        rospy.loginfo("Running script...")
       
        #listener = tf.TransformListener(True, rospy.Duration(10.0))
        #rospy.sleep(2)
        
        self.sss.say("sound", ["Enter a location Please"])
        
        goLocation = self.getLocation()
        
        if(len(goLocation)==2):
            print "------location: ", goLocation
            self.sss.say("sound", ["Location is found"])
        else:
            print "------ Some thing goes wrong ..."
            
        moveBase = self.sss.move("base", [goLocation[0],goLocation[1], 0.00], False, "omni")
        moveBase.wait()     
       
       
    def getLocation(self):
        location = raw_input("Please enter the Location: (example: table OR -2.221, 0.115): ")
        
        locationArray = location.split(',')
        print "--len--: ",len(locationArray)
        
        if(len(locationArray)==1):
            if(locationArray[0] == "table"):
                print "Location is found"
                locationArray = [-2.230, 0.089]
                print "return array for table: ",locationArray
                return locationArray     
                
            else:
                print "Location is not found... Try Again!!!"
                del locationArray[:]
                self.getLocation()
        
        elif(len(locationArray)==2):
            print "return 2: ",locationArray
            return locationArray
            
        else:
            print "Wrong Input...Try Again!!!"
            del locationArray[:]
            self.getLocation()
               
                 
     
    
if __name__ == '__main__':
    try:
        print "Start_Node Started"
        MyScript().Start()
                
        moveScript = MoveArm()
        moveScript.Start()
        
        mygrasps_node().Start()
        
        '''count = 0
        while not rospy.is_shutdown():
           # rate = rospy.Rate(1)
            #rate.sleep()
            if(count<3):
                print "-------------------- %s"%count
            elif(count ==3):  
                print "-------------------- script completed............" 
                
            count = count + 1'''
        
        
    except rospy.ROSInterruptException:
        pass
