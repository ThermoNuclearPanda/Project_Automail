import sys
import struct
from arduino_port import Arduino
from myo import Myo
from send_pose_listener import SendPoseListener
from vibration_type import VibrationType
import serial

def main():
	print('Starting MyoConnect')

	myo = Myo()
	listener = SendPoseListener()
	try:
		myo.connect()
		myo.add_listener(listener)
		print("listener added")
		myo.vibrate(VibrationType.SHORT)
		print("vibrated")
		while True:
			myo.run()

	except KeyboardInterrupt:
		pass
	except ValueError as ex:
		print(ex)
	finally:
		myo.safely_disconnect()
		print('Finished')
if __name__ == '__main__':
	main()
