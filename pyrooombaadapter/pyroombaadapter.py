"""
A Python module for Roomba Open Interface
"""
import math
from time import sleep

import byte_tool
import serial


class PyRoombaAdapter:
    """
    Adapter class for Roomba Open Interface

    The constructor connects serial port and change the mode to safe mode

    Args:
        - port: Serial port string
        - bau_rate (default=115200): bau rate of serial connection
        - time_out_sec (default=1.0) : read time out of serial connection [sec]
        - wheel_span_mm (default=235.0): wheel span of Roomba [mm]

    Examples:
        >>> PORT = "/dev/ttyUSB0"
        >>> adapter = PyRoombaAdapter(PORT)

    """
    CMD = {"Start": 128,
           "Baud": 129,
           "Safe": 131,
           "Full": 132,
           "Power": 133,
           "Spot": 134,
           "Clean": 135,
           "Max": 136,
           "Drive": 137,
           "Moters": 138,
           "Sensors": 142,
           "Seek Dock": 143,
           "PWM Moters": 144,
           "Drive Direct": 145,
           "Drive PWM": 146,
           "Query List": 149,
           "Stream": 148,
           }

    Packet_ID = {
        "OI Mode": 35,
    }

    PARAMS = {
        "STRAIGHT_RADIUS": 32768,
        "MIN_RADIUS": -2000,
        "MAX_RADIUS": 2000,
        "MIN_VELOCITY": -500,
        "MAX_VELOCITY": 500,
    }

    def __init__(self, port, bau_rate=115200, time_out_sec=1., wheel_span_mm=235.0):
        self.WHEEL_SPAN = wheel_span_mm
        self.serial_con = self._connect_serial(port, bau_rate, time_out_sec)

        self.change_mode_to_safe()  # default mode is safe mode

    def __del__(self):
        """
        Destructor of PyRoombaAdapter class

        The Destructor make Roomba move to passive mode and close serial connection
        """
        # disconnect sequence
        self._send_cmd(self.CMD["Start"])  # move to passive mode
        sleep(0.1)
        self.serial_con.close()

    def start_cleaning(self):
        """
        Start the default cleaning

        - Available in modes: Passive, Safe, or Full
        - Changes mode to: Passive

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.start_cleaning()
        """
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Clean"])

    def start_max_cleaning(self):
        """
        Start the max cleaning

        - Available in modes: Passive, Safe, or Full
        - Changes mode to: Passive

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.start_max_cleaning()
        """
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Max"])

    def start_spot_cleaning(self):
        """
        Start spot cleaning

        - Available in modes: Passive, Safe, or Full
        - Changes mode to: Passive

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.start_spot_cleaning()
        """
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Spot"])

    def start_seek_dock(self):
        """
        Start seek dock

        - Available in modes: Passive, Safe, or Full
        - Changes mode to: Passive

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.start_seek_dock()
        """
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Seek Dock"])

    def change_mode_to_passive(self):
        """
        Change mode to passive mode

        Roomba beeps once to acknowledge it is starting from “off” mode.

        - Available in modes: Passive, Safe, or Full
        """
        self._send_cmd(self.CMD["Start"])

        # TODO implement
        # check mode
        # self.request_data([self.Packet_ID["OI Mode"]])

    def change_mode_to_safe(self):
        """
        Change mode to safe mode

        Safe mode turns off all LEDs.
        If a safety condition occurs, Roomba reverts automatically to Passive mode.

        - Available in modes: Passive, Safe, or Full
        """
        # send command
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Safe"])

        # TODO implement
        # check mode
        # self.request_data([self.Packet_ID["OI Mode"]])

    def change_mode_to_full(self):
        """
        Change mode to full mode

        Full mode turns off the cliff, wheel-drop and internal charger safety features.
        In Full mode, Roomba executes any command that you send it, even if the internal charger is plugged in,
        or command triggers a cliff or wheel drop condition.

        - Available in modes: Passive, Safe, or Full
        """
        # send command
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Safe"])

        # TODO implement
        # check mode
        # self.request_data([self.Packet_ID["OI Mode"]])

    def turn_off_power(self):
        """
        Turn off power of Roomba

        The mode change to passive mode.

        - Available in modes: Passive, Safe, or Full

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.turn_off_power()
        """
        # send command
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Power"])

    def request_data(self, request_id_list):

        if len(request_id_list) == 1:  # single packet
            self._send_cmd(self.CMD["Start"])
            self._send_cmd(self.CMD["Sensors"])
            self._send_cmd(request_id_list[0])
            # print("re:", self.serial_con.read())
            # sleep(0.5)

    def move(self, velocity, yaw_rate):
        """
        control roomba at the velocity and the rotational speed (yaw rate)

        Note:
            The Roomba keep a control command until receiving next command

        - Available in modes: Safe or Full
        - Changes mode to: No Change
        - Velocity (-500 – 500 mm/s)
        - Radius (-2000 – 2000 mm)
        - Special cases:
            - Straight = 32768 or 32767 = hex 8000 or 7FFF
            - Turn in place clockwise = -1
            - Turn in place counter-clockwise = 1

        Args:
            - velocity: velocity (m/sec)
            - yaw_rate: yaw rate (rad/sec)

        Examples:
            >>> import numpy as np
            >>> import time
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.move(0, np.rad2deg(-10)) # rotate to right side
            >>> time.sleep(1.0) # keep rotate
            >>> adapter.move(0.1, 0.0) # move straight with 10cm/sec
        """
        if yaw_rate >= 0:
            direction = 'CCW'
        else:
            direction = 'CW'

        if velocity == 0:  # rotation
            vel_mm_sec = math.fabs(yaw_rate) * (self.WHEEL_SPAN / 2.0)
            radius_mm = 0
        elif yaw_rate == 0:
            vel_mm_sec = velocity * 1000.0  # m/s -> mm/s
            radius_mm = self.PARAMS["STRAIGHT_RADIUS"]
        else:
            vel_mm_sec = velocity * 1000.0  # m/s -> mm/s
            radius_mm = vel_mm_sec / yaw_rate

        self.send_drive_cmd(vel_mm_sec, radius_mm, direction)

    def send_drive_cmd(self, roomba_mm_sec, roomba_radius_mm, turn_dir='CCW'):
        """
        send drive command

        This command controls Roomba’s drive wheels.
        The radius is measured from the center of the turning circle to the center of Roomba.
        A Drive command with a positive velocity and a positive radius makes Roomba drive forward while turning toward the left.
        A negative radius makes Roomba turn toward the right.
        Special cases for the radius make Roomba turn in place or drive straight.
        A negative velocity makes Roomba drive backward.

        Args:
            - roomba_mm_sec: the average velocity of the drive wheels in millimeters per second (mm/s)
            - roomba_radius_mm: the radius in millimeters at which Roomba will turn.
            - turn_dir: turning direction, it should be CW:clock wise or CCW: counter clock wise
        """
        # print(roomba_mm_sec, roomba_radius_mm, turn_dir)

        roomba_mm_sec = self._adjust_velocity(roomba_mm_sec)
        velHighVal, velLowVal = byte_tool.get_2_bytes(roomba_mm_sec)

        roomba_radius_mm = self._adjust_radius(roomba_radius_mm, turn_dir)
        radiusHighVal, radiusLowVal = byte_tool.get_2_bytes(roomba_radius_mm)

        # send these bytes and set the stored velocities
        self._send_cmd([self.CMD["Drive"], velHighVal, velLowVal, radiusHighVal, radiusLowVal])

    @staticmethod
    def _connect_serial(port, bau_rate, time_out):
        serial_con = serial.Serial(port, baudrate=bau_rate, timeout=time_out)
        if serial_con.isOpen():
            print('Serial port is open, presumably to a roomba...')
        else:
            print('Serial port did NOT open')
        return serial_con

    def _adjust_radius(self, radius, turn_dir):

        if type(radius) != int:
            radius = int(radius)

        if radius < self.PARAMS["MIN_RADIUS"]:
            radius = self.PARAMS["STRAIGHT_RADIUS"]
        if radius > self.PARAMS["MAX_RADIUS"]:
            radius = self.PARAMS["STRAIGHT_RADIUS"]

        if radius == 0:
            if turn_dir == 'CW':
                radius = -1
            else:  # default is 'CCW' (turning left)
                radius = 1
        return radius

    def _adjust_velocity(self, velocity):

        if type(velocity) != int:
            velocity = int(velocity)

        if velocity < self.PARAMS["MIN_VELOCITY"]:
            velocity = self.PARAMS["MIN_VELOCITY"]
        elif velocity > self.PARAMS["MAX_VELOCITY"]:
            velocity = self.PARAMS["MAX_VELOCITY"]

        return velocity

    def _send_cmd(self, cmd):
        if type(cmd) == list:  # command list
            self.serial_con.write(bytes(cmd))
        else:  # one command
            self.serial_con.write(bytes([cmd]))


def main():
    PORT = "/dev/ttyUSB0"
    adapter = PyRoombaAdapter(PORT)
    adapter.turn_off_power()
    # sleep(1.0)
    # adapter.move(0, np.deg2rad(-10))
    # sleep(1.0)
    # adapter.move(0, np.deg2rad(10))
    # sleep(1.0)
    # adapter.move(0.1, np.deg2rad(0.0))
    # sleep(1.0)
    # adapter.move(-0.1, 0)
    # sleep(1.0)


if __name__ == '__main__':
    main()
