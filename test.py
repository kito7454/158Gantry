# moves from shelf to galvo then to keyence then to ir
from zaber_motion import Units
from zaber_motion.ascii import Connection, pvt

import buildGantree
import helpers.spcHelper as sh
import numpy as np
# import importantCoordinates
import time
# from zaber_motion.dto.ascii import MeasurementSequence
import helpers.gantryHelperAdvanced as gh
# import helpers.ahkHelper as ahk


gantreeFile = r"C:\Users\minok\PycharmProjects\gantryAutomation\curr_gantry.csv"
rt = buildGantree.buildGantree(gantreeFile)
# print(rt)

with Connection.open_serial_port("COM7") as connection:
    device_list = connection.detect_devices()
    # print(device_list)

    # device_Gantry = device_list[0]
    # device_Angle1 = device_list[1]
    # device_Angle2 = device_list[2]

    # gh.goTo(device_list, destination="point_1", end_orient=0, root=rt, move=True)
    #
    # time.sleep(2)

    # gh.pickupNamed(device_list=device_list, root=rt, location="shelf_in", distance_threshold_mm=500)
    # gh.dropoffNamed(device_list=device_list, root=rt, location="galvo_in", backwards=False, distance_threshold_mm=5)

    gh.goTo(device_list, destination="galvo_up", end_orient=0, root=rt, move=True)

    # gh.pickupNamed(device_list=device_list, root=rt, location="galvo_in", distance_threshold_mm=10)
    # gh.dropoffNamed(device_list=device_list, root=rt, location="shelf_in", backwards=False, distance_threshold_mm=5)

    # gh.dropoffNamed(device_list=device_list, root=rt, location="ocean_in", backwards=False, distance_threshold_mm=5,clearance=5)

    # gh.goTo(device_list, destination="ocean_in", end_orient=0, root=rt, move=True)
    #
    # gh.pickupNamed(device_list=device_list, root=rt, location="ocean_in", distance_threshold_mm=10,clearance=5)
    # gh.dropoffNamed(device_list=device_list, root=rt, location="raman_in", backwards=False, distance_threshold_mm=5)

    # gh.pickupNamed(device_list=device_list, root=rt, location="raman_in", distance_threshold_mm=10)
    # gh.dropoffNamed(device_list=device_list, root=rt, location="shelf_in", backwards=False, distance_threshold_mm=5)