#! /usr/bin/env python

#Make the node an executable node
#chmod u+x ~/catkin_ws/src/beginner_tutorials/src/projecttask1.py

import rospy
import sys
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

vel_msg = Twist()
vel_msg.linear.x = 0.5
vel_msg.angular.z = 0.0

speed = 0.5
walldistance = 0.6
obstacle = False
direction = 1
roundCounter = 0

nodeid = str(sys.argv[1])
nodename = 'robot_' + nodeid

rospy.init_node(nodename, anonymous=True)
pub = rospy.Publisher(nodename + '/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)

def rotate(speed, angle, clockwise, lspeed=0):
	rospy.loginfo("Rotating...")
	angularspeed = speed * (math.pi/180)
	relativeangle = angle * (math.pi/180)
	vel_msg.linear.x = lspeed
	vel_msg.angular.z = clockwise * angularspeed

	t0 = rospy.Time.now().to_sec()
	current_angle = 0

	while(current_angle < relativeangle):
		pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angularspeed * (t1-t0)
		rate.sleep()


	vel_msg.linear.x = 0.0
	vel_msg.angular.z = 0.0
	pub.publish(vel_msg)
		

def moveRobot():
	rospy.loginfo("Moving...")
	speed =0.5 
	global roundCounter
	if roundCounter < 3:
		distance = 1.0
	else:
		distance = 8.0

	vel_msg.linear.x = speed
	vel_msg.linear.y = 0.0
	vel_msg.linear.z = 0.0

	vel_msg.angular.x = 0.0
	vel_msg.angular.y = 0.0
	vel_msg.angular.z = 0.0

	t0 = rospy.Time.now().to_sec()
	current_distance = 0.0

	while(current_distance < distance):
		pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_distance = speed * (t1-t0)
		rate.sleep()

   	roundCounter = roundCounter + 1
	vel_msg.linear.x = 0.0
	vel_msg.angular.z = 0.0
	pub.publish(vel_msg)

def checkingObstacle():
	global obstacle
	while obstacle != True:
		vel_msg.linear.x = 0.5
		vel_msg.angular.z = 0.0
		pub.publish(vel_msg)
		rate.sleep()		
		
def round1():
	checkingObstacle()
	
 	if int(sys.argv[1]) == 0:
		direction = -1
	elif int(sys.argv[1]) == 1:
		direction = 1

	rotate(5.0,90.0,direction)
	moveRobot()
	rotate(5.0,90.0,direction)

def round2():
	checkingObstacle()

	if int(sys.argv[1])  == 0:
		direction = 1
	elif int(sys.argv[1]) == 1:
		direction = -1

	rotate(5.0,90.0,direction)
	moveRobot()
	rotate(5.0,90.0,direction)

def round3():
	checkingObstacle()
	
	if int(sys.argv[1]) == 0:
		direction = -1
	elif int(sys.argv[1]) == 1:
		direction = 1

	rotate(5.0,90.0,direction)
	moveRobot()
	rotate(5.0,90.0,direction)
	moveRobot()

def callback(msg):
	global obstacle 
	obstacle = False
	size = len(msg.ranges)	
	for i in range(0, size):
		if float(msg.ranges[i]) < walldistance and float(msg.ranges[i]) != 0.0:		
			obstacle = True

if __name__ == "__main__":
												
	sub = rospy.Subscriber(nodename+'/base_scan', LaserScan, callback)
	round1()
	round2()
	round3()

	rospy.spin()

