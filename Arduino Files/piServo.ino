/******************************************
* @Author: Kiran Gurajala & Alex Lee
* @Project: Project Automail
* @Version: 1.0
*
* Class Summary:
* The PiServo sketch runs on an Arduino
* Microchecks from its serial bytes of data
* '0'-'5'. By matching the incoming data
* with the corresponding pose function to
* handle, the sketch will actuate the hand
* based on pose input.
*******************************************/

#include <Servo.h>;
Servo rotator;        //Rotator will actuate the wrist rotation
Servo clencher;       //clencher will actuate the gripping motion

int refreshRate = 20; //in milliseconds; the time interval for the micro to check for incoming data through serial
int space = 5;        //this number serves as a standard servo's angle from reaching its maximum actuation
int input = 0;        //variable for the serial input

int rPos = 90;        //variable for rotator position; 90 represents rest position or neutral position
int cPos = space;     //variable for clencher position; 0 + space is rest position for clench.
int rotatorSpeed = 2;
int clencherSpeed = 2;//degree increment for the clencher Servo.

//rLED and cLED will light up when rotator and clencher servo are running respectively.
int rLED = 7;         //Pin number for Rotator LED
int cLED = 8;         //Pin number for Clencher LED

//Poses and its number assosciated for each one
const int REST = 0, FIST = 1, FINGERSPREAD = 4, WAVE_IN = 2, WAVE_OUT = 3, DOUBLE_TAP = 5;
const int STOP = 90, RIGHT = 93, LEFT = 87; //numbers to designate movement for a continuous servo

//-----------------------------------SETUP----------------------------------------------
void setup() {
  rotator.attach(11);      //Attach rotator and clencher servos
  clencher.attach(9);
  pinMode(rLED, OUTPUT);   //Set LEDs to OUTPUT
  pinMode(cLED, OUTPUT);
  Serial.begin(9600);
  startUp();               //Startup Sequence that sets the position of the hand to neutral position
}

//------------------------------------LOOP----------------------------------------------
void loop() {
  if (Serial.available() > 0) {      //check for incoming data
    input = Serial.read() - '0';     //read incoming byte scaled to 0
  }
  //Comparative process to assocsiate the byte with a specific pose
  if (input == REST) {
    rest();                          //do the pose "REST"
  } else if (input == FIST) {
    fist();
  } else if (input == FINGERSPREAD) {
    fingerspread();
  } else if (input == WAVE_IN) {
    waveIn();
  } else if (input == WAVE_OUT) {
    waveOut();
  }
  delay(refreshRate);                //How often to check for incoming data from Myo
}

//---------------------------------STARTUP-----------------------------------------------
void startUp() {                     //Startup sequence to set servos to neutral positions
  while (cPos != 90) {
    if (cPos > 90) {                 //Set clencher servo to neutral position (90)
      cPos --;
      clencher.write(cPos);
      cLEDOn();
    } else if (cPos < 90) {
      rPos ++;
      clencher.write(cPos);
      cLEDOn();
    }
    delay(15);
  }
  rLEDOff();                          //set LEDs to off state when Servos are not running
  cLEDOff();
}

//-----------------------------------FIST-------------------------------------------------
void fist() {
  if (cPos < 180 - space) { //if position of clencher is within the Servo boundaries
    cPos += clencherSpeed;  //increment the position of clench
    clencher.write(cPos);   //move clencher servo to new position
    cLEDOn();               //set clencher led to on
  }
}

//------------------------------FINGERSPREAD----------------------------------------------
void fingerspread() {
  if (cPos > space) {      //if position of clencher is above minimum threshold, decrease
    cPos -= clencherSpeed;
    clencher.write(cPos);
    cLEDOn();
  }
}

//----------------------------------REST---------------------------------------------------
void rest(){              //set servo motion to stop
   rotator.write(STOP);
   rLEDOff();
}

//---------------------------------WAVEIN--------------------------------------------------
void waveIn() {           //set servo motion to clockwise
  rotator.write(RIGHT);
  rLEDOn();
  cLEDOff();
}

//---------------------------------WAVEOUT-------------------------------------------------
void waveOut() {          //set servo motion to counterclockwise
  rotator.write(LEFT);
  rLEDOn();
  cLEDOff();
}

//---------------------------------RLEDON--------------------------------------------------
void rLEDOn() {           //set rotator LED to ON state
  digitalWrite(rLED, HIGH);
}

//---------------------------------RLEDOFF-------------------------------------------------
void rLEDOff() {          //set rotator LED to OFF state
  digitalWrite(rLED, LOW);
}

//---------------------------------CLEDON--------------------------------------------------
void cLEDOn() {           //set clencher LED to ON state
  digitalWrite(cLED, HIGH);
}

//---------------------------------CLEDOFF-------------------------------------------------
void cLEDOff() {          //set clencher LED to OFF state
  digitalWrite(cLED, LOW);
}
