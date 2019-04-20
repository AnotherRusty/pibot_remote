#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function



'''
    Robot manager works as a maintainer for robot status
    & an executer for execute any commands. Any real actions
    regarding the robot will be done by the robot manager.
'''

import sys
sys.path.append("..")
import pypibot
from pypibot import log
from pypibot import roslauncher
from Config import *
from RobotStatus import RobotStatus
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose, PoseWithCovarianceStamped
from std_srvs.srv import Empty
from threading import Lock, Thread
from time import time, sleep
from sys import exit
from pypibot import roslauncher

class RobotManager(object):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RobotManager, cls).__new__(cls, *args, **kwargs)
            cls.__initialized = False
        return cls._instance

    def init(self):
        if self.__initialized:
            return
        self.__initialized = True

        log.i('robot manager init')

        if LAUNCH_NAVIGATION:
            self.launch_nav = roslauncher.roslauncher(NAVIGATION_LAUNCH_CMD)
            self.launch_nav.launch()

        self.robot_speed = Twist()  # tempararily stores robot speed
        self.robot_pose = Pose()    # tempararily stores robot pose

        self.rs = RobotStatus()
        ### Robot Stauts Lock
        # - Used to protect all the data in robot_status
        # - Should always acquire/release this lock when doing something about robot_status.
        self.robot_status_lock = Lock()

        # ros
        rospy.init_node('robot_manager', anonymous=False)
        rospy.Subscriber('/odom', Odometry, self.odom_cb)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.init_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)

        if ROBOT_POSE_TYPE == ABSOLUTE:
            self.tf_listener = tf.TransformListener()
            try:
                self.tf_listener.waitForTransform('/map', '/base_link', rospy.Time(0), rospy.Duration(3.0))
            except (tf.Exception, tf.ConnectivityException, tf.LookupException) as e:
                log.e('wait for tf transform between /map and /base_link timeout %s'%e)
                return False

        # robot status update thread
        self.rs_update_rountine = Thread(target=self.rs_update, name='robot_status_update')
        self.rs_update_rountine.setDaemon(True)
        self.rs_update_rountine.start()
        
        if ROBOT_STATUS_DEBUG:
            self.rs_debug = Thread(target=self.rs_debug_print, name='robot_status_debug')
            self.rs_debug.setDaemon(True)
            self.rs_debug.start()
        return True

    def spin(self):
        rospy.spin()

    def odom_cb(self, odom):
        self.robot_speed.linear.x = odom.twist.twist.linear.x
        self.robot_speed.linear.y = odom.twist.twist.linear.y
        self.robot_speed.angular.z = odom.twist.twist.angular.z

        if ROBOT_POSE_TYPE == RELATIVE:
            self.robot_pose = odom.pose.pose

    def lookup_tf(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            if DEBUG:
                log.e('fail to lookup tf transformation. tf error')
            return 

        self.robot_pose.position.x = trans[0]
        self.robot_pose.position.y = trans[1]
        self.robot_pose.orientation.x = rot[0]
        self.robot_pose.orientation.y = rot[1]
        self.robot_pose.orientation.z = rot[2]
        self.robot_pose.orientation.w = rot[3]

    def rs_debug_print(self):
        now = time()
        while True:
            if time()-now > 1.0:
                if self.robot_status_lock.acquire():
                    log.d('speed - vx:',self.rs.vx, 'vy:', self.rs.vy, 'vw:', self.rs.vw)
                    log.d('pose - x:', self.rs.x, 'y:', self.rs.y, 'yaw:', self.rs.yaw)
                    self.robot_status_lock.release()
                now = time()

    def rs_update(self):
        '''
            Update velocities and pose to robot status
        '''
        interval = 1.0/ROBOT_STATUS_UPDATE_FREQUENCY
        now = time()

        while True:
            if (time()-now)>interval:
                if self.robot_status_lock.acquire():
                    # update velocities
                    self.rs.vx = self.robot_speed.linear.x
                    self.rs.vy = self.robot_speed.linear.y
                    self.rs.vw = self.robot_speed.angular.z

                    # update pose
                    if ROBOT_POSE_TYPE == ABSOLUTE:
                        self.lookup_tf()
                    if ROBOT_POSE_TYPE == RELATIVE:
                        pass
                    self.rs.x = self.robot_pose.position.x
                    self.rs.y = self.robot_pose.position.y
                    orientation = self.robot_pose.orientation
                    quat = [orientation.x, orientation.y, orientation.z, orientation.w]
                    self.rs.yaw = tf.transformations.euler_from_quaternion(quat)[-1]
                    self.robot_status_lock.release()
                    
                    log.t("v=[%f, %f, %f] pos=[%f, %f, %f]" %(self.rs.vx, self.rs.vy, self.rs.vw, self.rs.x, self.rs.y, self.rs.yaw))
                now = time()

    def get_speed(self):
        '''Get the current robot speeds.
        '''
        self.robot_status_lock.acquire()
        vx = self.rs.vx
        vy = self.rs.vy
        vw = self.rs.vw
        self.robot_status_lock.release()
        return (vx, vy, vw)

    def get_pose(self):
        '''Get the current robot pose.
        '''
        self.robot_status_lock.acquire()
        x = self.rs.x
        y = self.rs.y
        yaw = self.rs.yaw
        self.robot_status_lock.release()
        return (x, y, yaw)

    def set_vel(self, vx, vy, vw):
        '''Control the robot's speeds by publishing command to /cmd_vel topic.'''
        cmd = Twist()
        cmd.linear.x = vx
        cmd.linear.y = vy
        cmd.angular.z = vw
        self.cmd_vel_pub.publish(cmd)
    
    def set_pose(self, x, y, yaw):
        '''Set the robot pose'''
        pose = PoseWithCovarianceStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'map'
        pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
        pose.pose.pose.position.x = x
        pose.pose.pose.position.y = y
        quat = tf.transformations.quaternion_from_euler(0, 0, yaw)
        pose.pose.pose.orientation.x = quat[0]
        pose.pose.pose.orientation.y = quat[1]
        pose.pose.pose.orientation.z = quat[2]
        pose.pose.pose.orientation.w = quat[3]
        self.init_pose_pub.publish(pose)
        # clear costmap
        rospy.wait_for_service('/move_base/clear_costmaps')
        clear = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        try:
            clear()
        except rospy.ServiceException, e:
            print(e)
            