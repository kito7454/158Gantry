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

    device_Gantry = device_list[0]
    device_Angle1 = device_list[1]
    device_Angle2 = device_list[2]
    ax = device_Gantry.get_lockstep(1)
    print(device_list)


    gh.goTo(device_list,destination="midpoint",end_orient=0,root=rt,move=True)
    gh.pickupNamed(device_list=device_list, root=rt, location="shelf", distance_threshold_mm=10)
    gh.goTo(device_list, destination="midpoint", end_orient=0, root=rt, move=True)
    gh.dropoffNamed(device_list=device_list, root=rt, location="shelf", backwards=False, distance_threshold_mm=5)