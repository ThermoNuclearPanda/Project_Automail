"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""

# Required imports
import sys
from device_listener import DeviceListener
from pose_type import PoseType
from arduino_port import Arduino

class SendPoseListener(DeviceListener):

    def on_pose_arduino(self, pose, arduino):
        pose_type = PoseType(pose)
        print(pose_type.name)
        arduino.write(pose_type.value)

    def on_pose(self, pose):
        pose_type = PoseType(pose)
        print(pose_type.name)
