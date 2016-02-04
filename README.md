# Project Automail
    Automail is a Python application on raspberry pi that acts a bridge between the Myo armband and an Arduino.
    It achieves this by translating the electrical signals from the Myo over bluetooth to a number which is
    then passed on to an Arduino to produce a mechanical motion

## Raspberry Pi Setup

    Automail is meant to work on a raspberry pi with a linux operating system. Steps to set up are below

        1. Load a raspberry pi with a linux distro (we used raspbian)
        2. Install dependencies (see below)
        3. Configure the pi to boot to command line and auto login
        4. Add myoConnect.py to run at start up (see below for instructions)

Dependencies:
- Python Version 2.6 or greater
- pySerial
- enum34

AutoLogin and script on start up:
- http://www.opentechguides.com/how-to/article/raspberry-pi/5/raspberry-pi-auto-start.html

## Arduino Setup

    1. Install Arduino IDE (https://www.arduino.cc/en/Main/Software)
    2. Load piServo.uno onto your Arduino through the IDE

Note:
- You must change the Product ID (PID) in arduino_port.py (lines 25-27) to the one specific to your Arduino
```python

for port in portList:
        """ Note: PID is device specific, this is for arduino micro """
        if "VID:PID=2341:8037" in port[0]\
        or "VID:PID=2341:8037" in port[1]\
        or "VID:PID=2341:8037" in port[2]:
        return port[0]

```

## Caveats

- You must have the usb bluetooth adapter plugged in to the pi.
- You must calibrate your Myo armband with the Myo Connect software from Thalmic Labs before using Automail.
- You must sync the Myo before using it with Automail, it will vibrate for a brief period and then begin to execute
  your poses.

## Support

- If you have a question about the software or find an error, please open an issue, and I will get to it as I can.

## To Do

- An Arduino library for Myo without the need of a raspberry pi is being worked on
- A python package to bundle this together is also on its way

## Forking

- Fork away! please build with and upon Automail!

## License

- GNU GPL v3, see LICENSE.
- Please remember that no warranty, implied or explicit is included in this software.
