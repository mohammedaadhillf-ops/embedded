from controller import Supervisor, Keyboard
import math

TIME_STEP = 32

SAFE_DISTANCE = 2.5
CAUTION_DISTANCE = 5.0
MAX_SPEED = 0.055

robot = Supervisor()
keyboard = Keyboard()
keyboard.enable(TIME_STEP)

front = robot.getDevice("front_ultrasonic")
rear = robot.getDevice("rear_ultrasonic")
accel = robot.getDevice("mpu_accelerometer")
gyro = robot.getDevice("mpu_gyro")
display = robot.getDevice("oled")

green = robot.getDevice("green_led")
yellow = robot.getDevice("yellow_led")
red = robot.getDevice("red_led")

front.enable(TIME_STEP)
rear.enable(TIME_STEP)
accel.enable(TIME_STEP)
gyro.enable(TIME_STEP)

car = robot.getFromDef("SAFETY_CAR")
translation = car.getField("translation")
rotation = car.getField("rotation")

light_low = False
accident_demo = False
manual_stop = False
last_accident = False

def clamp_distance(value):
    if value <= 0.0 or value > 10.0:
        return 10.0
    return value

def set_leds(status):
    green.set(1 if status == "SAFE" else 0)
    yellow.set(1 if status == "CAUTION" else 0)
    red.set(1 if status in ("DANGER", "ACCIDENT") else 0)

def draw_oled(front_d, rear_d, acc_mag, status):
    display.setColor(0xFFFFFF)
    display.fillRectangle(0, 0, 320, 180)
    display.setColor(0x000000)
    display.setFont("Arial", 18, True)
    display.drawText("VEHICLE SAFETY", 12, 18)
    display.setFont("Arial", 14, False)
    display.drawText(f"FRONT: {front_d:4.1f} m", 12, 48)
    display.drawText(f"REAR : {rear_d:4.1f} m", 12, 70)
    display.drawText(f"ACC  : {acc_mag:4.2f} g", 12, 92)
    display.drawText("LIGHT: LOW" if light_low else "LIGHT: NORMAL", 12, 114)
    display.setFont("Arial", 17, True)
    display.drawText("STATUS: " + status, 12, 146)
    display.setFont("Arial", 11, False)
    display.drawText("L=light  A=accident  R=reset", 12, 168)

print("=== Intelligent Vehicle Safety Assistant - Webots 3D ===")
print("Controls: L = toggle low light, A = accident demo, R = reset, SPACE = stop/start")

while robot.step(TIME_STEP) != -1:
    # Keyboard controls
    key = keyboard.getKey()
    while key != -1:
        if key in (ord('L'), ord('l')):
            light_low = not light_low
            print("Light mode:", "LOW" if light_low else "NORMAL")
        elif key in (ord('A'), ord('a')):
            accident_demo = True
            print("ACCIDENT DEMO TRIGGERED")
        elif key in (ord('R'), ord('r')):
            accident_demo = False
            light_low = False
            manual_stop = False
            translation.setSFVec3f([0, 0.35, 4.5])
            rotation.setSFRotation([0, 1, 0, 0])
            print("System reset")
        elif key == Keyboard.SPACE:
            manual_stop = not manual_stop
        key = keyboard.getKey()

    # Sensor readings
    front_d = clamp_distance(front.getValue() / 100.0)
    rear_d = clamp_distance(rear.getValue() / 100.0)

    av = accel.getValues()
    gv = gyro.getValues()

    # Acceleration magnitude relative to gravity.
    acc_mag = math.sqrt(av[0]**2 + av[1]**2 + av[2]**2) / 9.81

    # Simple software accident demonstration.
    if accident_demo:
        status = "ACCIDENT"
    elif front_d < SAFE_DISTANCE or rear_d < SAFE_DISTANCE:
        status = "DANGER"
    elif front_d < CAUTION_DISTANCE or rear_d < CAUTION_DISTANCE:
        status = "CAUTION"
    else:
        status = "SAFE"

    # Automatic forward motion unless stopped or a safety condition is reached.
    pos = translation.getSFVec3f()
    if not manual_stop and not accident_demo and status != "DANGER":
        pos[2] -= MAX_SPEED
        if pos[2] < -4.0:
            pos[2] = 4.5
        translation.setSFVec3f(pos)

    # Tilt the car for the accident demonstration.
    if accident_demo:
        rotation.setSFRotation([0, 0, 1, 0.45])
    else:
        rotation.setSFRotation([0, 1, 0, 0])

    set_leds(status)
    draw_oled(front_d, rear_d, acc_mag, status)

    print(
        f"Front: {front_d:4.2f} m | Rear: {rear_d:4.2f} m | "
        f"Accel: {acc_mag:4.2f} g | Light: {'LOW' if light_low else 'NORMAL'} | "
        f"Status: {status}"
    )
