"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""

# Required imports
import re
from ble import BLE
from serial.tools.list_ports import comports
from utilities import *
from vibration_type import VibrationType


class Myo(object):

    # Initializes ble object and connection
    def __init__(self):
        self.ble = None
        self.connection = None

    # Disconnects and then finds bluetooth usb adapter && myo device
    def connect(self, tty_port = None):
        self.safely_disconnect()
        # Finds bluetooth adapter and myo device address
        self.find_bluetooth_adapter(tty_port)
        address = self.find_myo_device()

        print("received address from function")
        # Connects ble to myo
        connection_packet = self.ble.connect(address)
        self.connection = multiord(connection_packet.payload)[-1]
        self.ble.wait_event(3, 0)
        print('Connected.')

        # Validate myo object
        is_fw_valid = self.valid_firmware_version()

        if is_fw_valid:
            device_name = self.read_attribute(0x03)
            print('Device name: %s' % device_name.payload[5:])
            self.write_attribute(0x1d, b'\x01\x00')
            self.write_attribute(0x24, b'\x02\x00')
            self.initialize()
        else:
            raise ValueError('The firmware version must be v1.x or greater.')
    # Find Bluetooth adapter
    def find_bluetooth_adapter(self, tty_port = None):
        if tty_port is None:
            tty_port = self.find_tty()
        if tty_port is None:
            raise ValueError('Bluetooth adapter not found!')

        self.ble = BLE(tty_port)

    # Helper method to find tty port
    def find_tty(self):
        for port in comports():
            if re.search(r'PID=2458:0*1', port[2]):
                return port[0]

        return None

    # Runs and recieves packet while condition exists
    def run(self, timeout=None):
        if self.connection is not None:
            self.ble.receive_packet(timeout)
        else:
            raise ValueError('Myo device not paired.')

    # Helper method verify firmware version
    def valid_firmware_version(self):
        # Read firmware attribute
        firmware = self.read_attribute(0x17)
        _, _, _, _, major, minor, patch, build = unpack('BHBBHHHH', firmware.payload)

        print('Firmware version: %d.%d.%d.%d' % (major, minor, patch, build))

        return major > 0

    # Adds device listener
    def add_listener(self, listener):
        if self.ble is not None:
            self.ble.add_listener(listener)
        else:
            print('Connect function must be called before adding a listener.')

    # Vibrates myo
    def vibrate(self, duration):
        # initial vibrate UUID
        cmd = b'\x03\x01'
        # Concatenate vibrate UUID base with Vibration length
        if duration == VibrationType.LONG:
            cmd = cmd + b'\x03'
        elif duration == VibrationType.MEDIUM:
            cmd = cmd + b'\x02'
        elif duration == VibrationType.SHORT:
            cmd = cmd + b'\x01'
        else:
            cmd = cmd + b'\x00'
        # Write vibration attribute
        self.write_attribute(0x19, cmd)

    # Initialize myo object
    def initialize(self):
        self.write_attribute(0x28, b'\x01\x00')
        self.write_attribute(0x19, b'\x01\x03\x01\x01\x00')
        self.write_attribute(0x19, b'\x01\x03\x01\x01\x01')

    # Finds myo by connecting with ble object
    def find_myo_device(self):
        print('Find Myo device...')
        address = None
        print("before ble startscan")
        self.ble.start_scan()
        print("after ble startscan")
        while True:
            packet = self.ble.receive_packet()
            print("inside find myo loop")
            if packet.payload.endswith(b'\x06\x42\x48\x12\x4A\x7F\x2C\x48\x47\xB9\xDE\x04\xA9\x01\x00\x06\xD5'):
            print("package payload found!")
                address = list(multiord(packet.payload[2:8]))
                print("address found")
                break

        self.ble.end_scan()
        print("returning address")
        return address

    # Write attributes to myo with attributes and value
    def write_attribute(self, attribute, value):
        if self.connection is not None:
            self.ble.write_attribute(self.connection, attribute, value)

    # Read attribute from myo
    def read_attribute(self, attribute):
        if self.connection is not None:
            return self.ble.read_attribute(self.connection, attribute)
        return None

    # Graceful disconnect by removing ble object and disconnecting
    def safely_disconnect(self):
        if self.ble is not None:
            self.ble.end_scan()
            self.ble.disconnect(0)
            self.ble.disconnect(1)
            self.ble.disconnect(2)
            self.disconnect()

    # Disconnects current myo object
    def disconnect(self):
        if self.connection is not None:
            self.ble.disconnect(self.connection)