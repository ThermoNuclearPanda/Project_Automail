
"""
@Author: Kiran Gurajala & Alex Lee
@Project: Project Automail
@Version: 1.0
"""
# required imports
import sys
# Append Path
sys.path.append('../lib/')

import serial
import platform
import struct

class Arduino():
    # serial object initialized to null
    serial = None

    # Returns connected Arduino serial port
    def getPort(self):
        portList = list(serial.tools.list_ports.comports())
        for port in portList:
                """ Note: PID is device specific, this is for arduino micro """
            if "VID:PID=2341:8037" in port[0]\
                or "VID:PID=2341:8037" in port[1]\
                or "VID:PID=2341:8037" in port[2]:
                return port[0]

    # Connects to the Arduino
    def connect(self, port):
        global serial
        try:
            serial = serial.Serial(port, 9600)
        except SerialException:
            print("port already open")
        return serial

    # Writes to the Arduino
    def write(self, value):
        print(value)
        if(value == 0):
            serial.write('0')
        elif(value == 1):
            serial.write('1')
        elif(value == 2):
            serial.write('2')
        elif(value == 3):
            serial.write('3')
        elif(value == 4):
            serial.write('4')

    # Disconnects the Arduino
    def disconnect(self):
        if serialPort.isOpen():
            serialPort.close()

    def showReady(self):
        serial.write('6')
