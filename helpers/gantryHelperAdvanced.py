import time

from zaber_motion import Units
from zaber_motion.ascii import Connection, pvt
import pandas as pd
import numpy as np
# from zaber_motion.dto.ascii import MeasurementSequence
from zaber_motion.ascii import MeasurementSequence
from zaber_motion.ascii.pvt import PvtSequence
from zaber_motion.dto.ascii import PvtAxisType, PvtAxisDefinition


import gantree

# import spcHelper

# ------------------------
# define locations:
# import importantCoordinates
# import webSwitchHelper as wsh
# dummyLoc = importantCoordinates.dummyLoc
# piLoc = importantCoordinates.piLoc
# shelfLoc = importantCoordinates.shelfLoc
########################################
defaultTree = r"C:\Users\minok\PycharmProjects\gantryAutomation\curr_gantry.csv"



########################################
def connect(connection):
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))
    # target the xyz gantry
    device2 = device_list[1]

    # target the first rotation stage
    device3 = device_list[2]


def testMove(axis):
    axis.move_relative(25, Units.LENGTH_MILLIMETRES, True, 2000, Units.VELOCITY_MILLIMETRES_PER_SECOND, 1000,
                       Units.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED)


def pvtDrop(device_list, backwards=False):
    print("Found {} devices".format(len(device_list)))

    device_Gantry = device_list[0]
    device_Angle1 = device_list[1]
    device_Angle2 = device_list[2]

    all_axes = device_Gantry.all_axes
    all_axes.stop()

    pvt_buffer = device_Gantry.pvt.get_buffer(1)
    pvt_buffer.erase()
    pvt_ = device_Gantry.pvt
    pvt_sequence = pvt_.get_sequence(1)

    pvt_sequence.setup_live_composite(
        PvtAxisDefinition(1, PvtAxisType.PHYSICAL),
        PvtAxisDefinition(1, PvtAxisType.LOCKSTEP),
        PvtAxisDefinition(4, PvtAxisType.PHYSICAL)
    )

    if backwards:  # for some reason i accidentally flipped them but it works
        print("dropping backwards")
        pathPVT = r"C:\Users\minok\PycharmProjects\gantryAutomation\stageliftoffrelBackwards.csv"
        angle = 180

        angle2 = 180
        vel = 4.8
        del_theta = -14.4
    else:
        print("dropping")

        pathPVT = r"C:\Users\minok\PycharmProjects\gantryAutomation\stageliftoffrel.csv"
        angle = 0
        angle2 = 0
        vel = -4.8
        del_theta = 14.4

    data = pvt_sequence.load_sequence_data(pathPVT).sequence_data
    r1 = device_Angle1.get_axis(1)
    r2 = device_Angle2.get_axis(1)

    r2.move_absolute(angle2, Units.ANGLE_DEGREES, wait_until_idle=False)
    r1.move_absolute(angle, Units.ANGLE_DEGREES)
    r1.wait_until_idle()
    r2.wait_until_idle()

    # device_Angle1.move_velocity(vel, Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND)
    r1.move_relative(del_theta, Units.ANGLE_DEGREES, velocity=abs(vel),
                     velocity_unit=Units.ANGULAR_VELOCITY_DEGREES_PER_SECOND, wait_until_idle=False)
    pvt_sequence.points_relative(

        [MeasurementSequence(p.values[1:], p.unit) for p in data.positions],
        [MeasurementSequence(v.values[1:], v.unit) for v in data.velocities],
        MeasurementSequence(data.times.values[1:], data.times.unit)
    )

    # ?rotate stage?

    # pvt_sequence.call(pvt_buffer)

    time.sleep(2.5)
    r1.stop()
    r1.move_absolute(angle, Units.ANGLE_DEGREES)
    r1.wait_until_idle()

    all_axes.wait_until_idle(throw_error_on_fault=True)
    all_axes.stop()

    pvt_sequence.disable()


def xyzMove(device_Gantry, xpos, ypos, zpos, maxSpeed=200, maxAccel=100, zSpeed=25, wait_until_idle=True):
    # give xyz device ONLY
    # millimetres!!!!!
    ax = device_Gantry.get_axis(1) #horiz. short axis
    ay = device_Gantry.get_lockstep(1) #horiz. long axis
    az = device_Gantry.get_axis(4)  #vertical axis

    ax.move_absolute(xpos, Units.LENGTH_MILLIMETRES, False, maxSpeed, Units.VELOCITY_MILLIMETRES_PER_SECOND, maxAccel,
                     Units.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED)
    ay.move_absolute(ypos, Units.LENGTH_MILLIMETRES, False, maxSpeed, Units.VELOCITY_MILLIMETRES_PER_SECOND, maxAccel,
                     Units.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED)
    az.move_absolute(zpos, Units.LENGTH_MILLIMETRES, wait_until_idle, zSpeed, Units.VELOCITY_MILLIMETRES_PER_SECOND,
                     100,
                     Units.ACCELERATION_MILLIMETRES_PER_SECOND_SQUARED)

    all_axes = device_Gantry.all_axes

    if wait_until_idle:
        all_axes.wait_until_idle(throw_error_on_fault=wait_until_idle)


def rotate(device, axNum, angle, wait=True):
    # give xyz device ONLY
    # axis = 1 is for pitch axis, axis = 2 for roll axis
    # millimetres!!!!!
    az = device.get_axis(axNum)

    az.move_absolute(angle, Units.ANGLE_DEGREES, wait_until_idle=wait)


# pickups up the sample from specified coordinates [x,y,z] abs mm
# TODO: take in angle instead of backwards
def pickup(device, coordinates, backwards=False, clearance=5):
    # start 5mm away in z
    # xyzMove(device, coordinates[0], coordinates[1], coordinates[2]+5, 80, 50, 25)

    # actually pick up and wait for vacuum

    xyzMove(device, coordinates[0], coordinates[1], coordinates[2], 10, 50, 10)
    # wsh.switch(1)
    time.sleep(1)

    # lift away
    delx = 2
    if backwards:
        delx = -delx
    xyzMove(device, coordinates[0] + delx, coordinates[1] + delx, coordinates[2] + clearance, 20, 25, 10)


# TODO: take in angle instead of backwards
def pickupNamed(device_list, root, location, backwards=False, clearance=10, gantreeCsv=defaultTree, distance_threshold_mm=5):
    deviceGantry = device_list[0]

    angle = 0
    if backwards:
        angle = 180
    goTo(device_list = device_list,end_orient=angle, root=root, destination=location, gantreeCsv=gantreeCsv,
         distance_threshold_mm=distance_threshold_mm, move=True)

    coordinates = pollGantry(deviceGantry)
    xyzMove(deviceGantry, coordinates[0], coordinates[1], coordinates[2] + clearance, 10, 50, 10)
    # wsh.switch(1)
    time.sleep(1)
    # lift away
    delx = 2
    if backwards:
        delx = -delx
    xyzMove(deviceGantry, coordinates[0] + delx, coordinates[1] + delx, coordinates[2], 20, 25, 10)


# TODO: take in angle instead of backwards
def pickupBlind(device_list, backwards=False, clearance=10):
    device_Gantry = device_list[0]

    coordinates = pollGantry(device)
    xyzMove(device_Gantry, coordinates[0], coordinates[1], coordinates[2] + clearance, 10, 50, 10)

    time.sleep(1)
    # lift away
    delx = 2
    if backwards:
        delx = -delx
    xyzMove(device_Gantry, coordinates[0] + delx, coordinates[1] + delx, coordinates[2], 20, 25, 10)


# TODO: take in angle instead of backwards
def dropoff(device_list, coordinates, backwards=False):
    device = device_list[1]

    sign = 1
    if backwards:
        sign = -1
    xyzMove(device, coordinates[0] + 3 * sign, coordinates[1] + 3 * sign, coordinates[2] - 25, 100, 70, 150)
    xyzMove(device, coordinates[0] + 2 * sign, coordinates[1] + 2 * sign, coordinates[2] - 3, 50, 50, 50)
    xyzMove(device, coordinates[0], coordinates[1], coordinates[2], 10, 100, 10)

    pvtDrop(device_list, backwards)


# TODO: take in angle instead of backwards
def dropoffNamed(device_list, root, location, backwards=False, clearance=10, maxSpeed=250, gantreeCsv=defaultTree,
                 distance_threshold_mm=5):
    deviceGantry = device_list[0]

    angle = 0
    if backwards:
        angle = 180

    goTo(device_list = device_list, root=root, destination=location,end_orient=angle, gantreeCsv=gantreeCsv,
         distance_threshold_mm=distance_threshold_mm, move=True, maxSpeed=maxSpeed)
    coordinates = pollGantry(deviceGantry)
    sign = 1
    if backwards:
        sign = -1
    xyzMove(deviceGantry, coordinates[0] + 3 * sign, coordinates[1] + 3 * sign, coordinates[2], 100, 70, 150)
    xyzMove(deviceGantry, coordinates[0] + 2 * sign, coordinates[1] + 2 * sign, coordinates[2] + clearance + 2, 50, 50, 50)
    xyzMove(deviceGantry, coordinates[0], coordinates[1], coordinates[2] + clearance, 10, 100, 10)

    pvtDrop(device_list, backwards)
    xyzMove(deviceGantry, coordinates[0], coordinates[1], coordinates[2], 10, 100, 10)


# TODO: take in angle devices instead of backwards
def dropoffBlind(device_list, backwards=False, clearance=10):
    deviceGantry = device_list[0]
    device_Angle1 = device_list[1]
    device_Angle2 = device_list[2]

    coordinates = pollGantry(deviceGantry)
    sign = 1
    if backwards:
        sign = -1
    xyzMove(deviceGantry, coordinates[0] + 3 * sign, coordinates[1] + 3 * sign, coordinates[2], 100, 70, 150)
    xyzMove(deviceGantry, coordinates[0] + 2 * sign, coordinates[1] + 2 * sign, coordinates[2] + clearance - 2, 50, 50, 50)
    xyzMove(deviceGantry, coordinates[0], coordinates[1], coordinates[2] + clearance, 10, 100, 10)

    pvtDrop(device_list, backwards)
    xyzMove(deviceGantry, coordinates[0], coordinates[1], coordinates[2], 10, 100, 10)


# TODO
# takes zaber device and SPC client
# def dropOnPiStage(device,client):
# setPiPos(client,preset = "stage1gantry")
#
# c = importantCoordinates.piClose
# xyzMove(device, c[0], c[1], c[2], zSpeed=60)
#
# dropoff(device, importantCoordinates.piLocBig, backwards=False)
#
# setPiPos(client,preset = "stage1galvo")

# TODO
# def pickupPiStage(device,client):
# setPiPos(client,preset = "stage1gantry")
# time.sleep(2)
# pickup(device, importantCoordinates.piLocBig)



def navigate(device_list, root, pointA, pointB, end_orient, maxSpeed=250, move=False):
    if move:
        print("Found {} devices".format(len(device_list)))
        device_Gantry = device_list[0]
        device_Angle1 = device_list[1]
        device_Angle2 = device_list[2]
        start_orient = pollAngle(device_Angle1)
    else:
        start_orient = 0

    route = root.traverseWithOrientation(pointA, pointB, start_orient, end_orient)
    coords = gantree.routeToCoordinates(route)
    if move:
        for i in range(len(coords)):
            if isinstance(route[i], gantree.MoveArm):
                curr_point = route[i].end
                if curr_point > 170 or (curr_point < 10 and curr_point > -10) or curr_point < -170:
                    print('Moving second axis')
                    setAngles(device_list, curr_point, -curr_point)
                else:
                    print('Skipping second axis')
                    setAngles(device_list, curr_point, pollAngle(device=device4))
                print(route[i])
                continue
            print("Coordinates: " + str(coords[i]))
            xyzMove(device_Gantry=device_Gantry, xpos=coords[i][0], ypos=coords[i][1], zpos=coords[i][2], maxSpeed=maxSpeed,
                    maxAccel=200, zSpeed=250)
    else:
        print(route)


def setPiPos(client, stage=1, xval=0, yval=200, zval=16, preset=None):
    if preset is not None:
        if preset == "stage1gantry":
            xval = 0
            yval = 200
            zval = 16
        if preset == "stage1galvo":
            xval = 132.5
            yval = 33
            zval = 16.75
        if preset == "stage2gantry":
            xval = 200
            yval = 200
            zval = 0
            stage = 2

        if stage == 2:
            piX = "x2"
            piY = "y2"
            piZ = "z2"
        else:
            piX = "x1"
            piY = "y1"
            piZ = "z1"

    client.query("move " + piZ + " " + str(zval) + "\n")
    time.sleep(1)
    client.query("move " + piY + " " + str(yval) + "\n")
    time.sleep(1)
    client.query("move " + piX + " " + str(xval) + "\n")
    time.sleep(1)


def setAngles(device_list, angle=None, angle2=None):
    print("Found {} devices".format(len(device_list)))

    device_Gantry = device_list[0]
    device_Angle1 = device_list[1]
    device_Angle2 = device_list[2]

    all_axes = device_Gantry.all_axes
    all_axes.stop()

    r1 = device_Angle1.get_axis(1)
    r2 = device_Angle2.get_axis(1)

    if angle2 is not None:
        r2.move_absolute(angle2, Units.ANGLE_DEGREES, wait_until_idle=False)

    if angle is not None:
        r1.move_absolute(angle, Units.ANGLE_DEGREES)

    r1.wait_until_idle()
    r2.wait_until_idle()


def pollGantry(device_Gantry):
    # returns the positions of a devices axes
    ax = device_Gantry.get_axis(1) #horiz. short axis
    ay = device_Gantry.get_lockstep(1) #horiz. long axis
    az = device_Gantry.get_axis(4)  #vertical axis
    return [ax.get_position(Units.LENGTH_MILLIMETRES), ay.get_position(Units.LENGTH_MILLIMETRES),
            az.get_position(Units.LENGTH_MILLIMETRES)]


def pollAngle(device):
    # returns the positions of a devices axes
    a = device.get_axis(1)
    return a.get_position(Units.ANGLE_DEGREES)


def checkClosest(device, gantreeCsv=defaultTree):
    pos = pollGantry(device)
    df = pd.read_csv(gantreeCsv)
    distances = np.sqrt(
        (df['x'] - pos[0]) ** 2 +
        (df['y'] - pos[1]) ** 2 +
        (df['z'] - pos[2]) ** 2
    )

    # 4. Find the row with the minimum distance
    closest_idx = distances.idxmin()
    closest_row = df.loc[closest_idx]
    min_dist = distances.min()

    # if close point not found, check if in shelf:
    # special case if in shelf:
    # if min_dist > 24:
    #     s1_row = lookupCoordinates(key="shelf_one", gantreeCsv=defaultTree)
    #     in_shelf = all([
    #         abs(pos[0] - s1_row['x']) < 5,
    #         abs(pos[1] - s1_row['y']) < 610,  # Standardized to match X and Z
    #         abs(pos[2] - s1_row['z']) < 5
    #     ])
    #     if in_shelf:
    #         return {
    #             "name": "in_shelf",
    #             "distance": 1
    #         }

    return {
        "name": closest_row.key,
        "distance": min_dist
    }

    # print(f"Closest Entry:\n{closest_row}")
    # print(f"Distance: {min_dist}")


# def goTo(device, root, destination, maxSpeed=250, gantreeCsv=defaultTree, distance_threshold_mm=5, move=False):
#     # device: Zaber gantry device object
#     # root: Gantree data structure root
#     # Points: String Names of points to move from
#     # move: Supply as true if you want gantry to actually move
#     # farthest the gantry can be from a known point before throwing error
#
#     closest = checkClosest(device, gantreeCsv)
#     dist = closest.get("distance")
#     current_point = closest.get("name")
#     if current_point == "in_shelf":
#         shelfGoTo(device, root, 0)
#         closest = checkClosest(device, gantreeCsv)
#         dist = closest.get("distance")
#         current_point = closest.get("name")
#
#     if dist < distance_threshold_mm:
#         print("gantry found at: " + current_point)
#         navigate(device, root, current_point, destination, maxSpeed=maxSpeed, move=move)
#         print("moved to: " + destination)
#     else:
#         print(closest)
#         raise ValueError("gantry is lost.")


def goTo(device_list, root, destination, end_orient, maxSpeed=250, gantreeCsv=defaultTree, distance_threshold_mm=5,
         move=False):
    # connection: Zaber connection (Not just gantry device itself)
    # root: Gantree data structure root
    # Points: String Names of points to move from
    # end_orient: End orientation of gantry
    # move: Supply as true if you want gantry to actually move
    # farthest the gantry can be from a known point before throwing error


    # print(device_list)
    deviceGantry = device_list[0]

    closest = checkClosest(deviceGantry, gantreeCsv)
    dist = closest.get("distance")
    current_point = closest.get("name")
    # if current_point == "in_shelf":
    #     shelfGoTo(device, root, 0)
    #     closest = checkClosest(device, gantreeCsv)
    #     dist = closest.get("distance")
    #     current_point = closest.get("name")

    if dist < distance_threshold_mm:
        print("gantry found at: " + current_point)
        navigate(device_list, root, current_point, destination, end_orient=end_orient, maxSpeed=maxSpeed, move=move)
        print("moved to: " + destination)
    else:
        print(closest)
        raise ValueError("gantry is lost.")


def lookupCoordinates(key, gantreeCsv=defaultTree):
    df = pd.read_csv(gantreeCsv)
    print(key)
    print(df)
    return df.loc[df['key'] == key].iloc[0]


if __name__ == "__main__":
    with Connection.open_serial_port('COM6') as connection:
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device2 = device_list[1]

        # target the first rotation stage
        device3 = device_list[2]
        device4 = device_list[3]

        device = device2
        all_axes = device.all_axes
        all_axes.stop()

        pvt_buffer = device.pvt.get_buffer(1)
        pvt_buffer.erase()
        pvt_ = device.pvt
        pvt_sequence = pvt_.get_sequence(1)