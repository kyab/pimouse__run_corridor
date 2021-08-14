#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues
import math

class WallTrace():
    def __init__(self):
        self.cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber("/lightsensors", LightSensorValues, self.callback)

    def callback(self, messages):
        self.sensor_values = messages

    def run(self):
        rate = rospy.Rate(20)
        data = Twist() 

        accel = 0.005
        while not rospy.is_shutdown():
            s = self.sensor_values
            data.linear.x = accel

            if self.sensor_values.sum_all >= 50: data.linear.x = 0.0
            elif data.linear.x <= 0.05:          data.linear.x = 0.05
            elif data.linear.x >= 0.1:          data.linear.x = 0.1

            if data.linear.x < 0.1: data.angular.z = 0.0
            elif s.left_side < 10:  data.angular.z = 0.0
            else:
                target = 50
                error = (target - s.left_side)/50.0
                data.angular.z = error * 3 * math.pi / 180.0

            self.cmd_vel.publish(data)
            rate.sleep()

    def run2(self):
        rate = rospy.Rate(20)
        data = Twist()
        while not rospy.is_shutdown():
            # rospy.loginfo("goo")
            
            print("Hi")
            data.linear.x = 0.05
            data.angular.z = 0.0

            #stop with front wall
            if self.sensor_values.sum_all > 2000:
                data.linear.x = 0.0
                data.angular.z = 0.0
            elif self.sensor_values.left_side < 50:
                data.linear.x = 0.05
                data.angular.z = math.pi/20
            elif self.sensor_values.left_side > 300:
                data.linear.x = 0.05
                data.angular.z = -math.pi/4
            else:
                data.linear.x = 0.05
                data.angular.z = 0.0
            
            self.cmd_vel.publish(data)
            rate.sleep()

if __name__ == "__main__":
    rospy.init_node("wall_stop")
    rospy.wait_for_service("/motor_on")
    rospy.wait_for_service("/motor_off")
    rospy.loginfo("waitng for services.......done")
    rospy.on_shutdown(rospy.ServiceProxy("/motor/off", Trigger).call)
    rospy.ServiceProxy("/motor_on", Trigger).call()
    WallTrace().run2()


