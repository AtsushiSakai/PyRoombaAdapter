"""
A Python module for Roomba Open Interface

"""
import serial


class PyRoombaAdapter:
    CMD = {"Start": 128,
           "Baud": 129,
           "Safe": 131,
           "Full": 132,
           }

    def __init__(self, port, bau_rate=115200, time_out=0.5):
        self.serial_con = self._connect_serial(port, bau_rate, time_out)

    def __del__(self):
        self.serial_con.close()

    def change_mode_to_passive(self):
        # send command
        self._send_cmd(self.CMD["Start"])
        # check mode

    def request_data(self, request_id_list):

    @staticmethod
    def _connect_serial(port, bau_rate, time_out):
        serial_con = serial.Serial(port, baudrate=bau_rate, timeout=time_out)
        if serial_con.isOpen():
            print('Serial port is open, presumably to a roomba...')
        else:
            print('Serial port did NOT open, check the')
        return serial_con

    def _send_cmd(self, byte):
        self.serial_con.write(ord(byte))


def main():
    # PORT = "/dev/ttyUSB0"
    PORT = "/dev/ttyAMA0"
    adapter = PyRoombaAdapter(PORT)


if __name__ == '__main__':
    main()
