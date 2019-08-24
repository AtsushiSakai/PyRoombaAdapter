"""
    Play namidaga kirari by spitz
"""
from time import sleep

from pyroombaadapter import PyRoombaAdapter

PORT = "/dev/ttyUSB0"
adapter = PyRoombaAdapter(PORT)

adapter.send_song_cmd(0, 10,
                      [66, 67, 69, 67, 66, 62, 64, 66, 67, 66],
                      [16, 16, 16, 32, 32, 16, 16, 16, 16, 64])

sleep(1.0)
adapter.send_song_cmd(1, 9,
                      [66, 67, 69, 67, 66, 71, 59, 62, 61],
                      [16, 16, 16, 32, 32, 32, 16, 16, 64])

sleep(1.0)
adapter.send_song_cmd(2, 13,
                      [62, 64, 61, 62, 64, 66, 62, 64, 66, 67, 64, 66, 71],
                      [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16])
sleep(1.0)
adapter.send_song_cmd(3, 7,
                      [71, 67, 64, 62, 61, 62, 62],
                      [16, 16, 16, 16, 48, 16, 64])

sleep(3.0)
adapter.send_play_cmd(0)
sleep(4.0)
adapter.send_play_cmd(1)
sleep(4.0)
adapter.send_play_cmd(0)
sleep(4.0)
adapter.send_play_cmd(1)
sleep(4.0)
adapter.send_play_cmd(2)
sleep(4.0)
adapter.send_play_cmd(3)
sleep(4.0)
