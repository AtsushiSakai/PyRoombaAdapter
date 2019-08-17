from time import sleep

from pyroombaadapter import PyRoombaAdapter

PORT = "/dev/ttyUSB0"
adapter = PyRoombaAdapter(PORT)

# note names
f4 = 65
a4 = 69
c5 = 72
# note lengths
MEASURE = 160
HALF = int(MEASURE / 2)
Q = int(MEASURE / 4)
Ed = int(MEASURE * 3 / 16)
S = int(MEASURE / 16)

adapter.send_song_cmd(0, 9,
                      [a4, a4, a4, f4, c5, a4, f4, c5, a4],
                      [Q, Q, Q, Ed, S, Q, Ed, S, HALF])
adapter.send_play_cmd(0)
sleep(10.0)
