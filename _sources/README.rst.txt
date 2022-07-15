PyRoombaAdapter
===============

A Python library for Roomba Open Interface

|Downloads| |image1| |image2|

What is this?
=============

This is a python library for Roomba Open Interface(ROI)

This module is based on the document:

-  `iRobot® Roomba 500 Open Interface (OI)
   Specification <https://www.irobot.lv/uploaded_files/File/iRobot_Roomba_500_Open_Interface_Spec.pdf>`__

It aims to control a Roomba easily.

This module is only tested on Roomba 690 model.

Install
=======

You can use pip to install it.

::

   $ pip install pyroombaadapter

-  `pyroombaadapter ·
   PyPI <https://pypi.org/project/pyroombaadapter/>`__

Requirements
============

-  Python 3.6.x or higher (2.7 is not supported)

-  `pyserial <https://pythonhosted.org/pyserial/>`__

Documentation
=============

Please check the document for all API and usages.

-  `Welcome to PyRoombaAdapter’s
   documentation! <https://atsushisakai.github.io/PyRoombaAdapter/>`__

Usage examples
==============

All examples are in examples directory.

Click each image to see each example movie.

Go and back example
-------------------

|image3|

This example uses “move” API.

-  `move
   API <https://atsushisakai.github.io/PyRoombaAdapter/API.html#pyroombaadapter.PyRoombaAdapter.move>`__

.. code:: python

   """
       Go and back example with roomba
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

Play song1
----------

|image4|

This example uses “send_song_cmd” and “send_play_cmd” API.

-  `send_song_cmd
   API <https://atsushisakai.github.io/PyRoombaAdapter/API.html#pyroombaadapter.PyRoombaAdapter.send_song_cmd>`__

-  `send_play_cmd
   API <https://atsushisakai.github.io/PyRoombaAdapter/API.html#pyroombaadapter.PyRoombaAdapter.send_play_cmd>`__

.. code:: python

   """
       Play Darth Vader song
   """
   from time import sleep

   from pyroombaadapter import PyRoombaAdapter

   PORT = "/dev/ttyUSB0"
   adapter = PyRoombaAdapter(PORT)

   adapter.send_song_cmd(0, 9,
                         [69, 69, 69, 65, 72, 69, 65, 72, 69],
                         [40, 40, 40, 30, 10, 40, 30, 10, 80])
   adapter.send_play_cmd(0)
   sleep(10.0)

Play song2
----------

|image5|

This example uses “send_song_cmd” and “send_play_cmd” API.

-  `send_song_cmd
   API <https://atsushisakai.github.io/PyRoombaAdapter/API.html#pyroombaadapter.PyRoombaAdapter.send_song_cmd>`__

-  `send_play_cmd
   API <https://atsushisakai.github.io/PyRoombaAdapter/API.html#pyroombaadapter.PyRoombaAdapter.send_play_cmd>`__

.. code:: python

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

Read sensors
------------

There are two ways how to read sensor values. Request manually on
demand:

.. code:: python

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

Start a data stream:

.. code:: python

   """
       Read Roomba sensors
   """
   from time import sleep
   from pyroombaadapter import PyRoombaAdapter

   PORT = "/dev/ttyUSB0"
   adapter = PyRoombaAdapter(PORT)
   adapter.change_mode_to_passive()

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

Contribution
============

Any contributions to this project are welcome!

Feel free to make an issue and a PR to improve this OSS.

License
=======

MIT

Authors
=======

-  `Atsushi Sakai <https://github.com/AtsushiSakai/>`__

.. |Downloads| image:: https://pepy.tech/badge/pyroombaadapter
   :target: https://pepy.tech/project/pyroombaadapter
.. |image1| image:: https://pepy.tech/badge/pyroombaadapter/month
   :target: https://pepy.tech/project/pyroombaadapter
.. |image2| image:: https://pepy.tech/badge/pyroombaadapter/week
   :target: https://pepy.tech/project/pyroombaadapter
.. |image3| image:: https://img.youtube.com/vi/rGppIKN-roE/0.jpg
   :target: https://www.youtube.com/watch?v=rGppIKN-roE
.. |image4| image:: https://img.youtube.com/vi/0XqpQq7PQ8I/0.jpg
   :target: https://www.youtube.com/watch?v=0XqpQq7PQ8I
.. |image5| image:: https://img.youtube.com/vi/nYstniMkJo0/0.jpg
   :target: https://www.youtube.com/watch?v=nYstniMkJo0
