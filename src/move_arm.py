#!/usr/bin/python
import roslib
roslib.load_manifest('cob_script_server')

from simple_script_server import script

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf

#### Please change: cob_controller_configuration_gazebo/launch/robots/default_controllers_cob3-2.launch

class MoveArm(script):
       
    
    def Run(self):
        print "============ Move_arm_node Running =========================="
        self.istener = tf.TransformListener(True, rospy.Duration(10.0))
        rospy.sleep(2)
        
        objectGraspingPoint = self.getObject()
        print "Object grasping point = ",objectGraspingPoint        
        
        handle_arm = self.sss.move("arm","pregrasp")
        handle_arm.wait()
        handle_gripper = self.sss.move("gripper","cylopen", False)
        handle_gripper.wait()
         
        moveit_commander.roscpp_initialize(sys.argv)
        robot = moveit_commander.RobotCommander()
        
        scene = moveit_commander.PlanningSceneInterface()
        
        group = moveit_commander.MoveGroupCommander("arm")
        
        display_trajectory_publisher = rospy.Publisher(
                                            '/move_group/display_planned_path',
                                            moveit_msgs.msg.DisplayTrajectory)
        
        print "============ Waiting for RVIZ..."
        #rospy.sleep(10)
        print "============ Reference get_planning frame: %s" % group.get_planning_frame()
        print "============ Reference end_effector frame: %s" % group.get_end_effector_link()
        print "============ Reference end_effector frame: %s" % group.get_current_pose(group.get_end_effector_link())
        
        print "============ Robot Groups:"
        print robot.get_group_names()
        
        print "------------------- initial joint value: %s" %group.get_current_joint_values()
        
        
        print "============ Printing robot state"
        print robot.get_current_state()
        print " ====== ====== "
        
        ## Planning to a Pose goal
        ## ^^^^^^^^^^^^^^^^^^^^^^^
        oldPose = group.get_current_pose().pose
        print "OLD POSE: ", oldPose
        objectGraspingPoint = [-2.79, 0.095,1.04]
        #shaon end
        print "============ Generating plan 1"
        pose_target = geometry_msgs.msg.Pose()
        pose_target.orientation = oldPose.orientation
        pose_target.position.x = objectGraspingPoint[0] #-2.82 #-0.82 #-0.75
        pose_target.position.y = objectGraspingPoint[1] #0.08 #-0.070
        pose_target.position.z = objectGraspingPoint[2] #1.04 
        group.set_pose_target(pose_target)
        
        print "target POSE: ", pose_target
    
        group.plan()
        group.go(wait=True)
        
        
        
    def getObject(self):
        self.sss.say("sound", ["What do you want"])
        givenObject = raw_input("Please enter the Object Name (example: milk):  ")
        
        
        objectArray = givenObject.split(',')
        print "--len--: ",len(objectArray)
        
        objectlist = ["milk"]
        
        if(len(objectArray)==1):
            if(objectArray[0] == "milk"):
                print "Object is found"
                objectGraspingPoint = [-2.82, 0.08, 1.04]
                print "return 1: ",objectGraspingPoint
                return objectGraspingPoint
            
            elif(objectArray[0] == "list"):
                print "List of objects that has found: ", objectlist
                
            else:
                print "Location is not found... Try Again!!!"
                del objectArray[:]
                self.getObject()
            
        else:
            print "Wrong Input...Try Again!!!"
            del objectArray[:]
            self.getObject()
     
        
    
    

if __name__ == '__main__':
    try:
        print "hello World - cob moveit_group"
        
        SCRIPT = MoveArm()
        SCRIPT.Start()
        
        #mygrasps_node().Start()
        
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
