"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""

# Required imports
import serial
import time
from packet import Packet
from utilities import *
from arduino_port import Arduino

class BLE(object):

    # Initializes Arduino object
    def __init__(self, tty_port):
	self.arduino = Arduino()
	self.port = self.arduino.getPort()
	self.serial = self.arduino.connect(self.port)
        self.ser = serial.Serial(port=tty_port, baudrate=9600, timeout=3, dsrdtr=1)
        self.buffer = []
        self.listeners = []

    # Recieves Packet
    def receive_packet(self, timeout=None):
        start_time = time.time()
        self.ser.timeout = None
        while timeout is None or time.time() < start_time + timeout:
            if timeout is not None: self.ser.timeout = start_time + timeout - time.time()
            x = self.ser.read()
            if not x:
		print("no pose found")
		return None

            packet = self.process_byte(ord(x))
            if packet:
                if packet.data_type == 0x80:
                    self.notify_event_arduino(packet)
                return packet

    # Processes byte
    def process_byte(self, x):
        if not self.buffer:
            if x in [0x00, 0x80, 0x08, 0x88]:
                self.buffer.append(x)
            return None
        elif len(self.buffer) == 1:
            self.buffer.append(x)
            self.packet_length = 4 + (self.buffer[0] & 0x07) + self.buffer[1]
            return None
        else:
            self.buffer.append(x)

        if self.packet_length and len(self.buffer) == self.packet_length:
            packet = Packet(self.buffer)
            self.buffer = []
            return packet
        return None

    def notify_event(self, p):
	for listener in self.listeners:
	    if listener.__class__.__name__ == 'function':
		listener(p)
	    else:
		listener.handle_data(p)

    # Handle Arduino update
    def notify_event_arduino(self, p):
        for listener in self.listeners:
            if listener.__class__.__name__ == 'function':
                listener(p)
            else:
                listener.handle_data_arduino(p, self.arduino)

    # Add listener
    def add_listener(self, listener):
        self.listeners.append(listener)

    # Remove listener
    def remove_listener(self, listener):
        try: self.listeners.remove(listener)
        except ValueError: pass

    # Handle lapses packet
    def wait_event(self, cls, command):
        response = [None]
        def valid_packet(packet):
            if packet.cls == cls and packet.command == command:
                response[0] = packet
        self.add_listener(valid_packet)
        while response[0] is None:
            self.receive_packet()
        self.remove_listener(valid_packet)
        return response[0]
         
    def connect(self, address):
        return self.send_command(6, 3, pack('6sBHHHH', multichr(address), 0, 6, 6, 64, 0))

    def start_scan(self):
        return self.send_command(6, 2, b'\x01')

    def end_scan(self):
        return self.send_command(6, 4)

    def read_attribute(self, connection, attribute):
        self.send_command(4, 4, pack('BH', connection, attribute))
        return self.wait_event(4, 5)

    def write_attribute(self, connection, attribute, value):
        self.send_command(4, 5, pack('BHB', connection, attribute, len(value)) + value)
        return self.wait_event(4, 1)

    def send_command(self, cls, cmd, payload=b''):
        package = pack('4B', 0, len(payload), cls, cmd) + payload
        self.ser.write(package)

        while True:
            packet = self.receive_packet()

            if packet.data_type == 0:
                return packet

            self.notify_event(packet)

    def disconnect(self, h):
        return self.send_command(3, 0, pack('B', h))
