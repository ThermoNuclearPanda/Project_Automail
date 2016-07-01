"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""

# Required imports
from enum import Enum

# Enum class
class PoseType(Enum):
    REST = 0
    FIST = 1
    WAVE_IN = 2
    WAVE_OUT = 3
    FINGERS_SPREAD = 4
    DOUBLE_TAP = 5
    UNKNOWN = 255
