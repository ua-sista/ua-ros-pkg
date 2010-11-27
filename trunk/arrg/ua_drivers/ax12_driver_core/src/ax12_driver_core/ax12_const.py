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

"""
Dynamixel Constants
"""
# Control Table Constants
AX_MODEL_NUMBER_L = 0
AX_MODEL_NUMBER_H = 1
AX_VERSION = 2
AX_ID = 3
AX_BAUD_RATE = 4
AX_RETURN_DELAY_TIME = 5
AX_CW_ANGLE_LIMIT_L = 6
AX_CW_ANGLE_LIMIT_H = 7
AX_CCW_ANGLE_LIMIT_L = 8
AX_CCW_ANGLE_LIMIT_H = 9
DMXL_DRIVE_MODE = 10
AX_LIMIT_TEMPERATURE = 11
AX_DOWN_LIMIT_VOLTAGE = 12
AX_UP_LIMIT_VOLTAGE = 13
AX_MAX_TORQUE_L = 14
AX_MAX_TORQUE_H = 15
AX_RETURN_LEVEL = 16
AX_ALARM_LED = 17
AX_ALARM_SHUTDOWN = 18
AX_OPERATING_MODE = 19
AX_DOWN_CALIBRATION_L = 20
AX_DOWN_CALIBRATION_H = 21
AX_UP_CALIBRATION_L = 22
AX_UP_CALIBRATION_H = 23
AX_TORQUE_ENABLE = 24
AX_LED = 25
AX_CW_COMPLIANCE_MARGIN = 26
AX_CCW_COMPLIANCE_MARGIN = 27
AX_CW_COMPLIANCE_SLOPE = 28
AX_CCW_COMPLIANCE_SLOPE = 29
AX_GOAL_POSITION_L = 30
AX_GOAL_POSITION_H = 31
AX_GOAL_SPEED_L = 32
AX_GOAL_SPEED_H = 33
AX_TORQUE_LIMIT_L = 34
AX_TORQUE_LIMIT_H = 35
AX_PRESENT_POSITION_L = 36
AX_PRESENT_POSITION_H = 37
AX_PRESENT_SPEED_L = 38
AX_PRESENT_SPEED_H = 39
AX_PRESENT_LOAD_L = 40
AX_PRESENT_LOAD_H = 41
AX_PRESENT_VOLTAGE = 42
AX_PRESENT_TEMPERATURE = 43
AX_REGISTERED_INSTRUCTION = 44
AX_PAUSE_TIME = 45
AX_MOVING = 46
AX_LOCK = 47
AX_PUNCH_L = 48
AX_PUNCH_H = 49
DMXL_SENSED_CURRENT_L = 56
DMXL_SENSED_CURRENT_H = 57

# Status Return Levels
AX_RETURN_NONE = 0
AX_RETURN_READ = 1
AX_RETURN_ALL = 2

# Instruction Set
AX_PING = 1
AX_READ_DATA = 2
AX_WRITE_DATA = 3
AX_REG_WRITE = 4
AX_ACTION = 5
AX_RESET = 6
AX_SYNC_WRITE = 131

# Broadcast Constant
AX_BROADCAST = 254

# Error Codes
AX_INSTRUCTION_ERROR = 64
AX_OVERLOAD_ERROR = 32
AX_CHECKSUM_ERROR = 16
AX_RANGE_ERROR = 8
AX_OVERHEATING_ERROR = 4
AX_ANGLE_LIMIT_ERROR = 2
AX_INPUT_VOLTAGE_ERROR = 1
AX_NO_ERROR = 0

# Static parameters
DMXL_SPEED_RAD_SEC_PER_TICK = 0.011652344   # radians per second in one encoder unit
DMXL_MIN_SPEED_RAD = DMXL_SPEED_RAD_SEC_PER_TICK
DMXL_MAX_SPEED_RAD = 11.920347912           # maximum speed in radians per second

DMXL_MODEL_TO_NAME = \
{
    113: 'DX-113',
    116: 'DX-116',
    117: 'DX-117',
     12: 'AX-12+',
     18: 'AX-18F',
     10: 'RX-10',
     24: 'RX-24F',
     28: 'RX-28',
     64: 'RX-64',
    107: 'EX-106+',
}

KGCM_TO_NM = 0.0980665      # 1 kg-cm is that much N-m

# Holding torque in N-m
DMXL_MODEL_TO_TORQUE = \
{
    113: (12.0 / 10.2) * KGCM_TO_NM,        # 10.2 kg-cm @ 12V
    116: (12.0 / 21.4) * KGCM_TO_NM,        # 21.4 kg-cm @ 12V
    117: (12.0 / 15.0) * KGCM_TO_NM,        # 28.9 kg-cm @ 12V
     12: (12.0 / 15.0) * KGCM_TO_NM,        # 15.0 kg-cm @ 12V
     18: (12.0 / 18.0) * KGCM_TO_NM,        # 18.0 kg-cm @ 12V
     10: (12.0 / 13.0) * KGCM_TO_NM,        # 13.0 kg-cm @ 12V
     24: (12.0 / 26.0) * KGCM_TO_NM,        # 26.0 kg-cm @ 12V
     28: (18.5 / 37.0) * KGCM_TO_NM,        # 37.0 kg-cm @ 18.5V
     64: (18.5 / 52.0) * KGCM_TO_NM,        # 52.0 kg-cm @ 18.5V
    107: (18.5 / 107.0) * KGCM_TO_NM,       # 107.0 kg-cm @ 18.5V
}
