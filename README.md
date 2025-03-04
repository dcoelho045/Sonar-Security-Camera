# Sonar Security Camera 
This repository contains code and set up information for creating a Sonar Security Camera system. The goal of the project is to trigger a security camera to 
record when a person or group of persons has been detected approaching the sensor. By having the security camera turn on and being recording only when a trigger
has been detected, it allows the prevention unnecessary footage to be stored and assures that it will only record indiviudals who are approaching rather than 
falling branches, animals, or people passing by.


## Hardware 
The project uses a Raspberry Pi 4 as the central computer for which everything is hosted on. Connected to it is an HC-SR04 Sonar Sensor that uses sound to determine
its proximity to the object(s) infront of it. This is what's used to determine if a person is approaching. The Sonar Sensor is attached via breadboard and jumper cables.
A Raspberry Pi camera module is mounted directly to the Raspberry Pi and is used to capture the video footage.

## Software
A python script (securitycamera.py) kicks off two other python scripts that create and host a web server and the other starts the sonar camera system. Script sonarsensor.py runs the Sonar Sensor and triggers the camera module to begin recording when an indiviudal has been detected for a specific amount of time from a 
programmer/user defined distance. The camera records the video and stores it as a .mp4 file. The Raspberry Pi hosts a web server (app.py) that dynamically pushes the security 
footage to the web server that can be viewed by people who have the link and are on the same network. The web server displays the videos and allows the user to download files to their local machine if they'd like.
