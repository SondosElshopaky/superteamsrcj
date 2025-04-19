
from controller import Robot, GPS, Lidar, InertialUnit, DistanceSensor, Motor
import cv2
import numpy as np
import math
import struct

#region defines
###############################################################DEFINES######################################################################
#define robot
robot = Robot()
timeStep = 32
timestep = 32


# define motors
wheel_right = robot.getDevice("wheel1 motor") #wheel1
wheel_left = robot.getDevice("wheel2 motor") #wheel2


#reseting motors
wheel_right.setPosition(float('inf'))
wheel_left.setPosition(float('inf'))
wheel_right.setVelocity(0.0)
wheel_left.setVelocity(0.0)


#define sensors
imu = robot.getDevice("inertial_unit") #inertial_unit
gps = robot.getDevice("gps")
color = robot.getDevice("colour_sensor")
lidar = robot.getDevice("lidar")
#distance_sensor = robot.getDevice("distance sensor1")
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(timestep)


#enabling sensors
imu.enable(timestep)
gps.enable(timestep)
color.enable(timestep)
lidar.enable(timestep)
#distance_sensor.enable(timestep)


#define constants
max_velocity = 6.28
pi = math.pi


#define variables
velocity = max_velocity
compass_value=0
lidar_value=0
gps_readings = [0, 0, 0]
###################################################################################
def convert(deg):
    if deg < 0:

        Yaw2 = abs(deg)
        return Yaw2

    else:
        diff = 180 - deg
        Yaw2 = 180 + diff
        return Yaw2


def raycalculater(deg):
    deg = deg / 360
    deg = deg * 512
    deg +=1025
    return(deg)


def respawn():

    if receiver.getQueueLength() > 0:  # If receiver queue is not empty
        receivedData = receiver.getBytes()
        tup = struct.unpack('c', receivedData)  # Parse data into character
        if tup[0].decode("utf-8") == 'L':  # 'L' means lack of progress occurred
            print("Detected Lack of Progress!")
            receiver.nextPacket()
            return True
        receiver.nextPacket()  # Discard the current data packet



def correction():
    angles = imu.getRollPitchYaw()
    sa = convert(math.degrees(angles[2]))
    ea = 69  # Initial placeholder value
    dir = "bla"  # Initial placeholder direction

    # Correct direction assignments for each angle range
    if sa < 45:
        ea = 0
        dir = "R"  # Turn right (clockwise) towards 0
    elif 315 <= sa <= 360:
        ea = 0
        dir = "L"  # Turn left (counter-clockwise) towards 0
    elif 45 < sa <= 90:
        ea = 90
        dir = "L"  # Turn left towards 90
    elif 90 < sa <= 135:
        ea = 90
        dir = "R"  # Turn right towards 90
    elif 135 < sa <= 180:
        ea = 180
        dir = "L"  # Turn left towards 180
    elif 180 < sa <= 225:
        ea = 180
        dir = "R"  # Turn right towards 180
    elif 225 < sa <= 270:
        ea = 270
        dir = "R"  # Turn right towards 270
    elif 270 < sa <= 315:
        ea = 270
        dir = "L"  # Turn left towards 270

    # Handle ea wrapping over 360
    if ea > 359:  # Fixed syntax error: added colon
        ea -= 360

    ea1 = (ea - 0.5) % 360
    ea2 = (ea + 0.5) % 360

    while robot.step(timestep) != -1:
        angles = imu.getRollPitchYaw()
        Yaw = math.degrees(angles[2])
        ca = convert(Yaw)

        # Set wheel velocities based on direction
        if dir == "L":
            wheel_left.setVelocity(-1)
            wheel_right.setVelocity(1)
        elif dir == "R":
            wheel_left.setVelocity(1)
            wheel_right.setVelocity(-1)

        # Check if current angle is within target range considering wrap-around
        # Compute minimal difference
        diff = abs(ca - ea)
        min_diff = min(diff, 360 - diff)
        if min_diff <= 0.5:
            wheel_left.setVelocity(0.0)
            wheel_right.setVelocity(0.0)
            break

        # Handle overshoot
        current_diff = (ca - ea + 360) % 360  # Compute direction-aware difference
        if dir == "R":
            # Turning right (clockwise), expect current_diff to decrease
            if current_diff > 180:  # Overshoot in the wrong direction
                wheel_left.setVelocity(-1)
                wheel_right.setVelocity(1)
                # Allow time to correct (may need additional loop iterations)
        elif dir == "L":
            # Turning left (counter-clockwise), expect current_diff to increase
            if current_diff < 180:  # Overshoot in the wrong direction
                # Reverse direction to correct
                wheel_left.setVelocity(1)
                wheel_right.setVelocity(-1)
                # Allow time to correct (may need additional loop iterations)






def turnr():
    angles = imu.getRollPitchYaw()
    sa = convert(math.degrees(angles[2]))
    ea = sa + 90
    # print("1.sa:", sa, " ea:", ea)
    if ea > 360:
        ea -= 360
        # print("2.sa:", sa, "ea", ea)

    ea1 = ea - 1
    ea2 = ea + 1
    # print("3.sa:", sa, " ea", ea)

    while robot.step(timestep) != -1:
        angles = imu.getRollPitchYaw()
        Yaw = math.degrees(angles[2])
        ca = convert(Yaw)
        # print("4.sa:", sa, " ca", ca, " ea", ea)
        wheel_left.setVelocity(-5.0)
        wheel_right.setVelocity(5.0)
        # print("5.sa:", sa, " ca", ca, " ea", ea)
        # print("set wheel speeds")
        if ea1 <= ca <= ea2:
            # print("in if condition")
            # print("6.sa:", sa, " ca", ca, " ea", ea)
            wheel_left.setVelocity(0.0)
            wheel_right.setVelocity(0.0)
            # print("stopped")
            break



def turnl():
    angles = imu.getRollPitchYaw()
    sa = convert(math.degrees(angles[2]))
    ea = sa - 90
    # print("1.sa:", sa, " ea:", ea)
    if ea < 0:
        ea += 360
        # print("2.sa:", sa, "ea", ea)

    ea1 = ea - 1
    ea2 = ea + 1
    # print("3.sa:", sa, " ea", ea)

    while robot.step(timestep) != -1:
        angles = imu.getRollPitchYaw()
        Yaw = math.degrees(angles[2])
        ca = convert(Yaw)
        # print("4.sa:", sa, " ca", ca, " ea", ea)
        wheel_left.setVelocity(5.0)
        wheel_right.setVelocity(-5.0)
        # print("5.sa:", sa, " ca", ca, " ea", ea)
        # print("set wheel speeds")
        if ea1 <= ca <= ea2:
            # print("in if condition")
            # print("6.sa:", sa, " ca", ca, " ea", ea)
            wheel_left.setVelocity(0.0)
            wheel_right.setVelocity(0.0)
            # print("stopped")
            break



def movefront():  # need delay in beginning to work min 2 scs
    angles = imu.getRollPitchYaw()  # Step 4: Use the getValue() function to get the sensor reading
    angles = convert(math.degrees(angles[2]))
    ###################################### NORTH ##############################################
    if 1 > angles or angles > 359:
        zcurrent = round(gps.getValues()[2], 3)
        zfinish = zcurrent - 0.12
        # print("1.current", zcurrent, " end:", zfinish)
        while robot.step(timestep) != -1:
            zcurrent = imu.getRollPitchYaw()
            zcurrent = round(gps.getValues()[2], 3)
            # print("2.current", zcurrent, " end:", zfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (zfinish - 0.001) <= zcurrent <= (zfinish + 0.001):
                # print("3.current", zcurrent, " end:", zfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break


    ########################################## EAST ###############################################
    elif 89 <= angles <= 91:
        # print("entered if condtion")
        xcurrent = round(gps.getValues()[0], 3)
        xfinish = xcurrent + 0.12
        # print("1.current", xcurrent, " end:", xfinish)
        while robot.step(timestep) != -1:
            xcurrent = imu.getRollPitchYaw()
            xcurrent = round(gps.getValues()[0], 3)
            # print("2.current", xcurrent, " end:", xfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (xfinish - 0.001) <= xcurrent <= (xfinish + 0.001):
                # print("3.current", xcurrent, " end:", xfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break


    ########################################## WEST ###############################################
    elif 269 <= angles <= 271:
        # print("entered if condtion")
        xcurrent = round(gps.getValues()[0], 3)
        xfinish = xcurrent - 0.12
        # print("1.current", xcurrent, " end:", xfinish)
        while robot.step(timestep) != -1:
            xcurrent = imu.getRollPitchYaw()
            xcurrent = round(gps.getValues()[0], 3)
            # print("2.current", xcurrent, " end:", xfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (xfinish - 0.001) <= xcurrent <= (xfinish + 0.001):
                # print("3.current", xcurrent, " end:", xfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break
    ############################################# SOUTH #############################################
    elif 179 <= angles <= 181:
        # print("entered if condtion")
        zcurrent = round(gps.getValues()[2], 3)
        zfinish = zcurrent + 0.12
        # print("1.current", zcurrent, " end:", zfinish)
        while robot.step(timestep) != -1:
            zcurrent = round(gps.getValues()[2], 3)
            # print("2.current", zcurrent, " end:", zfinish)
            wheel_left.setVelocity(5.0)
            wheel_right.setVelocity(5.0)
            # print("started moving")
            if (zfinish - 0.001) <= zcurrent <= (zfinish + 0.001):
                # print("3.current", zcurrent, " end:", zfinish)
                wheel_left.setVelocity(0.0)
                wheel_right.setVelocity(0.0)
                # print("stopped and done")
                break
    else:
        correction()
        print("not in any directions >3")


def moveForward(steps):
    while steps > 0:
        movefront()
        steps -= 1

def moveLeft(steps):
    turnl()
    moveForward(steps)

def moveRight(steps):
    turnr()
    moveForward(steps)
    

def go_to_the_left_tile():
    moveForward(2)
    moveRight(1)
    moveLeft(1)
    moveLeft(2)
    moveRight(1)
    moveLeft(2)
    moveLeft(3)
    moveLeft(1)
    moveRight(2)
    moveRight(1)
    moveLeft(2)
    moveRight(1)
    moveLeft(1)
