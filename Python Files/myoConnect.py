"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""
# Required imports
import sys
import struct
from arduino_port import Arduino
from myo import Myo
from send_pose_listener import SendPoseListener
from vibration_type import VibrationType
import serial

def main():

	print('Starting MyoConnect')
	# Instantiate myo and listener objects
	myo = Myo()
	listener = SendPoseListener()

	try:
		# Connect myo and listner
		myo.connect()
		myo.add_listener(listener)
		print("listener added")
		# Vibrate armband when connected
		myo.vibrate(VibrationType.SHORT)
		print("vibrated")
		# Run myo
		while True:
			myo.run()

	# Error handling
	except KeyboardInterrupt:
		pass
	except ValueError as ex:
		print(ex)
	finally:
		myo.safely_disconnect()
		print('Finished')

# Run Driver 
if __name__ == '__main__':
	main()
