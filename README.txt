# Intelligent Vehicle Safety Assistant - Webots 3D Prototype

This is an educational 3D extension of the ESP32 vehicle-safety project.

## What is simulated
- Front and rear ultrasonic-style distance sensors
- MPU6050-equivalent accelerometer + gyroscope
- OLED-style dashboard display
- Green/yellow/red safety LEDs
- Low-light mode
- Accident/tilt demonstration
- Automatic vehicle movement toward a front obstacle

## Controls
- L = toggle LOW/NORMAL light
- A = trigger ACCIDENT demonstration
- R = reset the car and system
- SPACE = stop/start automatic motion

## Open
Use Webots R2025a or a compatible newer build.
Open:
worlds/vehicle_safety.wbt

The controller is:
controllers/vehicle_safety_controller/vehicle_safety_controller.py

## Important
This is a 3D concept simulation. It is not a replacement for the Wokwi ESP32 circuit simulation or the physical prototype. The LDR is represented by a keyboard-controlled software light mode, because this simple Webots model does not electrically model the ESP32/LDR circuit.
