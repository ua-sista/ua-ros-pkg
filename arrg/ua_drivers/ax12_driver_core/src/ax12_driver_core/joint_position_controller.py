#!/usr/bin/env python
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Arizona Robotics Research Group,
# University of Arizona. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of University of Arizona nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import roslib
roslib.load_manifest('ax12_driver_core')

import rospy
import math
from ax12_driver_core.ax12_const import *
from ax12_driver_core.ax12_user_commands import *
from ax12_driver_core.msg import MotorStateList
from ax12_driver_core.srv import SetSpeed
from ax12_driver_core.srv import TorqueEnable
from ua_controller_msgs.msg import JointState
from ua_controller_msgs.msg import JointStateList
from std_msgs.msg import Float64

class JointPositionControllerAX12:
    def __init__(self, out_cb, param_path):
        self.running = False
        self.send_packet_callback = out_cb
        self.topic_name = param_path
        self.joint_name = rospy.get_param(self.topic_name + '/joint_name')
        self.motor_id = rospy.get_param(self.topic_name + '/motor/id')
        self.initial_position_raw = rospy.get_param(self.topic_name + '/motor/init')
        self.min_angle_raw = rospy.get_param(self.topic_name + '/motor/min')
        self.max_angle_raw = rospy.get_param(self.topic_name + '/motor/max')

        self.flipped = self.min_angle_raw > self.max_angle_raw

        if self.flipped:
            self.min_angle = (self.initial_position_raw - self.min_angle_raw) * AX_RAD_RAW_RATIO
            self.max_angle = (self.initial_position_raw - self.max_angle_raw) * AX_RAD_RAW_RATIO
        else:
            self.min_angle = (self.min_angle_raw - self.initial_position_raw) * AX_RAD_RAW_RATIO
            self.max_angle = (self.max_angle_raw - self.initial_position_raw) * AX_RAD_RAW_RATIO

        self.speed_service = rospy.Service(self.topic_name + '/set_speed', SetSpeed, self.process_set_speed)
        self.torque_service = rospy.Service(self.topic_name + '/torque_enable', TorqueEnable, self.process_torque_enable)

    def initialize(self):
        # verify that the expected motor is connected and responding
        available_ids = rospy.get_param('ax12/connected_ids', [])
        if not self.motor_id in available_ids:
            rospy.logwarn("The specified motor id is not connected and responding.")
            rospy.logwarn("Available ids: %s" % str(available_ids))
            rospy.logwarn("Laser Tilt id: %d" % self.motor_id)
            return False

        self.set_speed(AX_MAX_SPEED_RAD)
        return True

    def start(self):
        self.running = True
        self.joint_state_pub = rospy.Publisher(self.topic_name + '/state', JointStateList)
        self.command_sub = rospy.Subscriber(self.topic_name + '/command', Float64, self.process_command)
        self.motor_states_sub = rospy.Subscriber('motor_states', MotorStateList, self.process_motor_states)

    def stop(self):
        self.running = False
        self.joint_state_pub.unregister()
        self.motor_states_sub.unregister()
        self.command_sub.unregister()
        self.speed_service.shutdown('normal shutdown')
        self.torque_service.shutdown('normal shutdown')

    def set_speed(self, speed):
        if speed < 0: speed = 0
        elif speed > AX_MAX_SPEED_RAD: speed = AX_MAX_SPEED_RAD
        speed_raw = int(round((speed / AX_MAX_SPEED_RAD) * AX_MAX_POSITION))
        mcv = (self.motor_id, speed_raw if speed_raw > 0 else 1)
        self.send_packet_callback((AX_GOAL_SPEED, [mcv]))

    def process_set_speed(self, req):
        self.set_speed(req.speed)

    def process_torque_enable(self, req):
        mcv = (self.motor_id, req.torque_enable)
        self.send_packet_callback((AX_TORQUE_ENABLE, [mcv]))

    def process_motor_states(self, state_list):
        if self.running:
            state = filter(lambda state: state.id == self.motor_id, state_list.motor_states)
            if state:
                state = state[0]
                joint_state = JointState(self.joint_name,
                                         self.raw_to_rad(state.position),
                                         (state.speed / AX_TICKS) * AX_MAX_SPEED_RAD,
                                         [self.motor_id],
                                         state.moving)
                self.joint_state_pub.publish([joint_state])

    def process_command(self, msg):
        angle = msg.data
        if angle < self.min_angle: angle = self.min_angle
        elif angle > self.max_angle: angle = self.max_angle
        mcv = (self.motor_id, self.rad_to_raw(angle))
        self.send_packet_callback((AX_GOAL_POSITION, [mcv]))

    def rad_to_raw(self, angle):
        """ angle is in radians """
        print "flipped = %s, angle_in = %f, init_raw = %d" % (str(self.flipped), angle, self.initial_position_raw)
        angle_raw = angle * AX_RAW_RAD_RATIO
        print 'angle = %f, val = %d' % (math.degrees(angle), int(round(self.initial_position_raw - angle_raw if self.flipped else self.initial_position_raw + angle_raw)))
        return int(round(self.initial_position_raw - angle_raw if self.flipped else self.initial_position_raw + angle_raw))

    def raw_to_rad(self, raw):
        return (self.initial_position_raw - raw if self.flipped else raw - self.initial_position_raw) * AX_RAD_RAW_RATIO
