# automatically gets spectral data on a grid
# start experiment with the spectrometer touching the (0,0) square with the (0,0) square facing away from both yellow encoders)

import serial
import pandas as pd
# import seabreeze.pyseabreeze
# import seabreeze.spectrometers
# import matplotlib.pyplot as plt
import numpy as np
import time


NUM_X = 8
NUM_Y = 8 # Grid size
STEP_X = 5.5         # mm
STEP_Y = 5.5         # mm
Z_HOP = 0.1           # mm
WAIT_TIME = 1       # Seconds to wait at top of Z

# important positions after homing:
loading = [48,0,0]
exp_start = [39.5,31.8,0]


def read_response(ser):
    """
    Read the response from the Corvus controller.

    :param ser: Serial object
    :return: Response string
    """
    response = ser.readline().decode().strip()
    return response
def get_initial_position(ser):
    ser.reset_input_buffer()
    ser.write(b"pos\r\n")
    time.sleep(.1)
    if ser.in_waiting:
        response = ser.readline().decode().strip()
        parts = response.split()
        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
        print(f"Initial Position Recorded: {x}, {y}, {z}")
        return (x, y, z)
    return None
def return_to_initial_position(ser, start_position):
    x, y, z = start_position
    z = z- Z_HOP
    print(f"Returning to Initial Position: {x}, {y}, {z}")
    command = f"{x} {y} {z} m\r\n"
    ser.write(command.encode())
    time.sleep(1)
    print("Successfully Returned")
def send_command(ser, command):
    """
    Send a command to the Corvus controller.
    Matches convention of serial_com.
    """
    ser.write(f"{command}\r\n".encode())
    time.sleep(1)


def read_response(ser):
    """
    Read response from controller.
    Matches convention of serial_com.
    """
    if ser.in_waiting:
        return ser.readline().decode().strip()
    return ""


def move_relative(ser, x, y, z):
    """
    Moves the stage relative to current position.
    Calculates sleep time based on distance.
    """
    send_command(ser, "2 sv")
    send_command(ser, "2 sa")

    command = f"{x} {y} {z} rmove"
    send_command(ser, command)

    max_dist = max(abs(x), abs(y), abs(z))
    sleep_time = (max_dist)/1.5 + 0.5
    time.sleep(sleep_time)


    # Calculate dynamic sleep: (Distance / Speed) + Buffer
    # Assuming standard speed ~10mm/s. Adjust divisor if needed.




def ramanMovement():
    try:

        dim = 9 #how many squares on each substrate
        step = 5 #mm spacing between squares

        ser = serial.Serial('COM5', 57600, timeout=1)
        time.sleep(1)  # Wait for handshake
        print(f"Connected: {ser.name}")
        # clear buffer
        ser.reset_input_buffer()
        start_position = get_initial_position(ser)
        print(start_position)

        for i in range(dim):
            for j in range(dim):
                move_relative(ser, step , 0, 0)  # Down
                time.sleep(0.5)
            move_relative(ser, 0, step, 0)  # Down
            move_relative(ser, -step*dim, 0, 0)  # Down
        move_relative(ser, 0, -step*dim, 0)  # Down

        ser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def testMovement():
    try:

        ser = serial.Serial('COM5', 57600, timeout=1)
        time.sleep(1)  # Wait for handshake
        print(f"Connected: {ser.name}")
        # clear buffer
        ser.reset_input_buffer()
        start_position = get_initial_position(ser)
        print(start_position)

        move_relative(ser, -20, 0, 0)  # Down
        time.sleep(1)

        ser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # testMovement()
    # ramanMovement()
    with serial.Serial('COM5', 57600, timeout=1) as ser:
        # send_command(ser, "cal")
        get_initial_position(ser)
        send_command(ser, "1 j")
        time.sleep(2)
        # ser.close()
