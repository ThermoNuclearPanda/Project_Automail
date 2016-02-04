# Project Automail
    Automail is a Python application that acts a bridge between the Myo armband and an Arduino.

##Setup

    Automail is meant to work on a raspberry pi with a linux operating system. Steps to set up are below

    <u> Raspberry Pi: </u>
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

    <u> Arduino: </u>
        - Install Arduino IDE (https://www.arduino.cc/en/Main/Software)
        - Load piServo.uno onto your Arduino through the IDE
