from utilities import *

class DeviceListener(object):

	def handle_data(self, data):
		if data.cls != 4 and data.command != 5:
			return

		connection, attribute, data_type = unpack('BHB', data.payload[:4])
		payload = data.payload[5:]

		if attribute == 0x23:
			data_type, value, address, _, _, _ = unpack('6B', payload)

			if data_type == 3:
				self.on_pose(value)

	def handle_data_arduino(self, data, arduino):
		if data.cls != 4 and data.command !=5:
			print("Leaving function")
			return

		connection, attribute, data_type = unpack('BHB', data.payload[:4])
		payload = data.payload[5:]
		if attribute == 0x23:
			data_type, value, address, _, _, _ = unpack('6B', payload)
			if data_type == 3:
				self.on_pose_arduino(value, arduino)

	def on_pose(self, pose):
		print("2")
		pass
	def on_pose_arduino(self, pose, arduino):
		print("3")	
		pass
	
