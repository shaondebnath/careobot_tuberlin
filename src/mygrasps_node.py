#!/usr/bin/python
import rospy

from simple_script_server import script
import tf

class mygrasps_node(script):
    def Run(self):
        print "============= mygrasp_node running ====================" 
        rospy.loginfo("Initializing all components...")
        
        components_to_init = ['arm', "gripper"]
        
        for component in components_to_init:
            self.sss.init(component)
            
        self.istener = tf.TransformListener(True, rospy.Duration(10.0))
        rospy.sleep(2)
                
        if not self.sss.parse:
                        
            self.sss.move("gripper","cylclosed",False)
            self.sss.sleep(2.2)
            self.sss.stop("gripper", "cylclosed")
        
            #hold object    
            self.sss.move("arm","hold")
        
            # keep it on tray
            self.sss.move("tray","up")
            handle_arm = self.sss.move("arm","grasp-to-tray",False)
            handle_arm.wait()
            self.sss.move("arm","overtray")
            self.sss.move("gripper","cylopen")
            
            handle_arm = self.sss.move("arm","tray-to-folded",False)
            handle_arm.wait()
            self.sss.move("gripper","home", False)
            
            moveBase = self.sss.move("base", [0.0, 0.0, 0.00], False, "omni")
            moveBase.wait()
            
            self.sss.say("sound", ["Here is your order"])
            
            

if __name__=='__main__':
    try:
        print "====Grasp Now" 
        #mygrasps_node().Start()
    except rospy.ROSInterruptException:
        pass