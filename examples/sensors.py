"""
    Read Roomba sensors
"""
from time import sleep
from pyroombaadapter import PyRoombaAdapter

PORT = "/dev/ttyUSB0"
adapter = PyRoombaAdapter(PORT)
adapter.change_mode_to_passive()

# Request sensor value manually
print(adapter.request_charging_state())
print(adapter.request_voltage())
print(adapter.request_current())
print(adapter.request_temperature())
print(adapter.request_charge())
print(adapter.request_capacity())
print(adapter.request_oi_mode())
print(adapter.request_distance())
print(adapter.request_angle())

# Read sensor value from data stream
adapter.data_stream_start(
    ["Charging State", "Voltage", "Current", "Temperature", "Battery Charge", "Battery Capacity", "OI Mode"])
sleep(1)
print(adapter.data_stream_read())
sleep(1)
print(adapter.data_stream_read())
sleep(1)
print(adapter.data_stream_read())
sleep(1)
adapter.data_stream_stop()
