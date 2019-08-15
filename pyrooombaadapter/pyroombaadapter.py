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
           "Spot": 134,
           "Clean": 135,
           "Max": 136,
           "Drive": 137,
           "Sensors": 142,
           "Seek Dock": 143,
           "Query List": 149,
           "Stream": 149,
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

    def change_mode_to_safe(self):
        # send command
        self._send_cmd(self.CMD["Start"])
        self._send_cmd(self.CMD["Safe"])

        # check mode
        # self.request_data([self.Packet_ID["OI Mode"]])

        # self._send_cmd(self.CMD["Start"])
        # self._send_cmd(self.CMD["Start"])
        # self._send_cmd(self.CMD["Safe"])

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

        Args:
            - velocity: velocity (m/sec)
            - yaw_rate: yaw raete (rad/sec)

        Examples:
            >>> PORT = "/dev/ttyUSB0"
            >>> adapter = PyRoombaAdapter(PORT)
            >>> adapter.move(0, -10) # rotate to right side
        """
        if yaw_rate >= 0:
            direction = 'CCW'
        else:
            direction = 'CW'

        if velocity == 0:  # rotation
            vel_mm_sec = math.fabs(yaw_rate) * (self.WHEEL_SPAN / 2.0)
            radius_mm = 0
        elif yaw_rate == 0:
            vel_mm_sec = velocity / 1000.0  # m/s -> mm/s
            radius_mm = self.PARAMS["STRAIGHT_RADIUS"]
        else:
            vel_mm_sec = velocity / 1000.0  # m/s -> mm/s
            radius_mm = vel_mm_sec / yaw_rate

        self._send_drive_cmd(vel_mm_sec, radius_mm, direction)

    def _send_drive_cmd(self, roomba_mm_sec, roomba_radius_mm, turn_dir='CCW'):
        """
        """
        print(roomba_mm_sec, roomba_radius_mm)

        roomba_mm_sec = self._adjust_velocity(roomba_mm_sec)
        velHighVal, velLowVal = byte_tool.get_2_bytes(roomba_mm_sec)

        roomba_radius_mm = self._adjust_radius(roomba_radius_mm, turn_dir)
        radiusHighVal, radiusLowVal = byte_tool.get_2_bytes(roomba_radius_mm)

        # send these bytes and set the stored velocities
        # self._send_cmd(self.CMD["Start"])
        # self._send_cmd(self.CMD["Safe"])
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
    adapter.start_max_cleaning()
    sleep(1.0)
    adapter.change_mode_to_safe()
    sleep(1.0)
    adapter.move(0, -10)
    sleep(1.0)
    adapter.move(0, 10)
    sleep(1.0)
    adapter.move(10, 0)
    sleep(1.0)
    adapter.move(-10, 0)
    sleep(1.0)


if __name__ == '__main__':
    main()
