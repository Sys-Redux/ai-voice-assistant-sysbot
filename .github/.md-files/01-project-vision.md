<!--markdownlint-disable-->
# SysBot -- AI Voice Assistant on Wheels

An AI voice assistant run on a raspberry pi 5 stationed on top of a body with wheels.

## Part 1 - Voice Assistant

On the raspberry Pi 5 (with speakers and microphone) we will create an app that
runs AI (dropdown menu to choose local or API) and is always listening. When the
app hears you talking to it, it will use the AI to answer you. The voice assistant
app will have a screen that displays the assistant (which is a cat robot), we
will accomplish this by using animations broken up into frames. Each group of
frames will represent the cat robot "listening", "thinking", "speaking", "idle",
etc.

## Part 2 - Robot in Motion

The screen of the voice assistant (which is it's head) will be on top of a body with wheels. The wheels
use DC motors to move. It's head will be able to turn left & right via a servo
motor. Will will need to attach an AI camera to the head so the robot will be able
to see where its going & where I am. The purpose of the robot having wheels and
being able to see is so that it can follow me around. The motion could either be
controlled by the same raspberry pi 5 as the voice assistant or it could use a
raspberry pi 0 2 (we would just have to connect the 0 & 5).

# Part 3 - Manual Control

The robot is intended to move on its own to follow me but I also want to have a
way to take control. We will accomplish this by developing an app to use on my
phone where if I take control I will be able to control the robots motion.