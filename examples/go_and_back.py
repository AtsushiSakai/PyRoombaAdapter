"""
    Go and  back example with roomba
"""
from time import sleep

import numpy as np
from pyroombaadapter import PyRoombaAdapter

PORT = "/dev/ttyUSB0"
adapter = PyRoombaAdapter(PORT)
adapter.move(0.2, np.deg2rad(0.0))  # go straight
sleep(1.0)
adapter.move(0, np.deg2rad(-20))  # turn right
sleep(6.0)
adapter.move(0.2, np.deg2rad(0.0))  # go straight
sleep(1.0)
adapter.move(0, np.deg2rad(20))  # turn left
sleep(6.0)
