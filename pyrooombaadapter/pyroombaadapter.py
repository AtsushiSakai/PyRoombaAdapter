"""
A Python adapter module for Roomba Open Interface

This module is based on the document: iRobot® Roomba 500 Open Interface (OI) Specification
- Link https://www.irobot.lv/uploaded_files/File/iRobot_Roomba_500_Open_Interface_Spec.pdf

"""
import math
from enum import Enum
from time import sleep

import byte_tool
import serial  # pyserial


class PyRoombaAdapter:
    """
    Adapter class for Roomba Open Interface

    The constructor connects serial port and change the mode to safe mode

    :param string port: Serial port path

    :param int bau_rate: bau rate of serial connection (default=115200)

    :param float time_out_sec: read time out of serial connection [sec] (default=1.0)

    :param float wheel_span_mm: wheel span of Roomba [mm]  (default=235.0)

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

    class Direction(Enum):
        clockwise = 1
        counter_clockwise = 2

    def __init__(self, port, bau_rate=115200, time_out_sec=1., wheel_span_mm=235.0):
        self.WHEEL_SPAN = wheel_span_mm
        self.serial_con = self._connect_serial(port, bau_rate, time_out_sec)

        self.change_mode_to_safe()  # default mode is safe mode
        sleep(1.0)

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

        - Special cases:
            - Straight = 32768 or 32767 = hex 8000 or 7FFF
            - Turn in place clockwise = -1
            - Turn in place counter-clockwise = 1

        :param float velocity: velocity (m/sec)

        :param float yaw_rate: yaw rate (rad/sec)

        Examples:
            >>> import numpy as np
            >>> import time
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.move(0, np.rad2deg(-10)) # rotate to right side
            >>> time.sleep(1.0) # keep rotate
            >>> adapter.move(0.1, 0.0) # move straight with 10cm/sec
        """
        if velocity == 0:  # rotation
            vel_mm_sec = math.fabs(yaw_rate) * (self.WHEEL_SPAN / 2.0)
            if yaw_rate >= 0:
                radius_mm = 1
            else:  # default is 'CCW' (turning left)
                radius_mm = -1
        elif yaw_rate == 0:
            vel_mm_sec = velocity * 1000.0  # m/s -> mm/s
            radius_mm = self.PARAMS["STRAIGHT_RADIUS"]
        else:
            vel_mm_sec = velocity * 1000.0  # m/s -> mm/s
            radius_mm = vel_mm_sec / yaw_rate

        self.send_drive_cmd(vel_mm_sec, radius_mm)

    def send_drive_cmd(self, roomba_mm_sec, roomba_radius_mm):
        """
        send drive command

        This command controls Roomba’s drive wheels.
        The radius is measured from the center of the turning circle to the center of Roomba.
        A Drive command with a positive velocity and a positive radius makes Roomba drive forward while turning left.
        A negative radius makes Roomba turn toward the right.
        Special cases for the radius make Roomba turn in place or drive straight.
        A negative velocity makes Roomba drive backward.

        :param float roomba_mm_sec: the average velocity of the drive wheels in millimeters per second (-500 – 500 mm/s)

        :param float roomba_radius_mm: the radius in millimeters at which Roomba will turn. (-2000 – 2000 mm)

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.send_drive_cmd(-100, -1000) # back to the right side
            >>> sleep(2.0) # keep 2 sec
        """
        # print(roomba_mm_sec, roomba_radius_mm, turn_dir)

        roomba_mm_sec = self._adjust_min_max(roomba_mm_sec, self.PARAMS["MIN_VELOCITY"], self.PARAMS["MAX_VELOCITY"])
        velHighVal, velLowVal = byte_tool.get_2_bytes(roomba_mm_sec)

        roomba_radius_mm = self._adjust_min_max(roomba_radius_mm, self.PARAMS["MIN_RADIUS"], self.PARAMS["MAX_RADIUS"])
        radiusHighVal, radiusLowVal = byte_tool.get_2_bytes(roomba_radius_mm)

        # send these bytes and set the stored velocities
        self._send_cmd([self.CMD["Drive"], velHighVal, velLowVal, radiusHighVal, radiusLowVal])

    def send_drive_direct(self, right_mm_sec, left_mm_sec):
        """
        send drive direct command

        This command lets you control the forward and backward motion of Roomba’s drive wheels independently.
        A positive velocity makes that wheel drive forward, while a negative velocity makes it drive backward.

        - Available in modes: Safe or Full

        :param float right_mm_sec: the velocity of the right drive wheels in millimeters per second (-500 – 500 mm/s)

        :param float left_mm_sec: the velocity of the left drive wheels in millimeters per second (-500 – 500 mm/s)

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.send_drive_direct(10, 100) # move right forward
            >>> sleep(2.0) # keep 2 sec
        """
        right_mm_sec = self._adjust_min_max(right_mm_sec, self.PARAMS["MIN_VELOCITY"], self.PARAMS["MAX_VELOCITY"])
        right_high, right_low = byte_tool.get_2_bytes(right_mm_sec)

        left_mm_sec = self._adjust_min_max(left_mm_sec, self.PARAMS["MIN_VELOCITY"], self.PARAMS["MAX_VELOCITY"])
        left_high, left_low = byte_tool.get_2_bytes(left_mm_sec)

        # send these bytes and set the stored velocities
        self._send_cmd([self.CMD["Drive Direct"], right_high, right_low, left_high, left_low])

    def send_drive_pwm(self, right_pwm, left_pwm):
        """
        send drive pwm command

        This command lets you control the forward and backward motion of Roomba’s drive wheels independently.
        It takes four data bytes, which are interpreted as two 16-bit signed values using two’s complement.
        A positive PWM makes that wheel drive forward, while a negative PWM makes it drive backward.

        - Available in modes: Safe or Full

        :param int right_pwm: Right wheel PWM (-255 – 255)

        :param int left_pwm: Left wheel PWM (-255 - 255)

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.send_drive_pwm(-200, -200) # move backward
            >>> sleep(2.0) # keep 2 sec
        """
        right_pwm = self._adjust_min_max(right_pwm, -255, 255)
        right_high, right_low = byte_tool.get_2_bytes(right_pwm)

        left_pwm = self._adjust_min_max(left_pwm, -255, 255)
        left_high, left_low = byte_tool.get_2_bytes(left_pwm)

        # send these bytes and set the stored velocities
        self._send_cmd([self.CMD["Drive PWM"], right_high, right_low, left_high, left_low])

    def send_moters_cmd(self, main_brush_on, main_brush_direction_is_ccw,
                        side_brush_on, side_brush_direction_is_inward,
                        vacuum_on
                        ):
        """
        send moters command

        This command controls the motion of Roomba’s main brush, side brush, and vacuum independently.
        Motor velocity cannot be controlled with this command, all motors will run at maximum speed when enabled.
        The main brush and side brush can be run in either direction. The vacuum only runs forward.

        :param bool main_brush_on: main brush on or off

        :param bool main_brush_direction_is_ccw: main brush direction, clockwise or counter-clockwise(default)

        :param bool side_brush_on: side brush on or off

        :param bool side_brush_direction_is_inward: side brush direction, inward(default) or outward

        :param bool side_brush_on: side brush on or off

        :param bool vacuum_on: vacuum on or off

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.send_moters_cmd(False, True, True, True, False) # side brush is on, and it rotates inward
            >>> sleep(2.0) # keep 2 sec
        """
        cmd = 0  # All initial bit is 0
        if side_brush_on:
            cmd |= 0b00000001
        if vacuum_on:
            cmd |= 0b00000010
        if main_brush_on:
            cmd |= 0b00000100
        if not side_brush_direction_is_inward:
            cmd |= 0b00001000
        if not main_brush_direction_is_ccw:
            cmd |= 0b00010000

        self._send_cmd([self.CMD["Moters"], cmd])

    @staticmethod
    def _connect_serial(port, bau_rate, time_out):
        serial_con = serial.Serial(port, baudrate=bau_rate, timeout=time_out)
        if serial_con.isOpen():
            print('Serial port is open, presumably to a roomba...')
        else:
            print('Serial port did NOT open')
        return serial_con

    @staticmethod
    def _adjust_min_max(val, min_val, max_val):

        # integer cast
        if type(val) != int:
            val = int(val)

        if val < min_val:
            val = min_val
        elif val > max_val:
            val = max_val

        return val

    def _send_cmd(self, cmd):
        if type(cmd) == list:  # command list
            self.serial_con.write(bytes(cmd))
        else:  # one command
            self.serial_con.write(bytes([cmd]))


def main():
    PORT = "/dev/ttyUSB0"
    adapter = PyRoombaAdapter(PORT)
    # adapter.send_drive_cmd(-100, -1000)
    # adapter.send_drive_direct(-100, 100)
    # import numpy as np
    # adapter.move(0.1, np.deg2rad(-10))
    # adapter.send_drive_pwm(80, 80)
    # adapter.send_drive_pwm(-200, -200)
    adapter.send_moters_cmd(False, True, True, True, False)
    sleep(1.0)

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
