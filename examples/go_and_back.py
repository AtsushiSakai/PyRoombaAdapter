"""
    Go and  back example with roomba
"""
from time import sleep

import math
from pyroombaadapter import PyRoombaAdapter

PORT = "/dev/ttyUSB0"
adapter = PyRoombaAdapter(PORT)
adapter.move(0.2, math.radians(0.0))  # go straight
sleep(1.0)
adapter.move(0, math.radians(-20))  # turn right
sleep(6.0)
adapter.move(0.2, math.radians(0.0))  # go straight
sleep(1.0)
adapter.move(0, math.radians(20))  # turn left
sleep(6.0)

#Print the total distance traveled
print(f"distance: {adapter.request_distance()} mm, angle: {adapter.request_angle()} rad")