<img src="https://github.com/AtsushiSakai/PyRoombaAdapter/raw/master/docs/icon.png?raw=true" align="right" width="300"/>

# PyRoombaAdapter

A Python library for Roomba Open Interface

# What is this?

This is a python library for Roomba Open Interface(ROI)

This module is based on the document:

- [iRobot® Roomba 500 Open Interface (OI) Specification](https://www.irobot.lv/uploaded_files/File/iRobot_Roomba_500_Open_Interface_Spec.pdf)

It aims to control a Roomba easily.

This module is only tested on Roomba 690 model. 

# Install

You can use setup.py to install it.

    $ git clone https://github.com/AtsushiSakai/PyRoombaAdapter.git

    $ sudo python PyRoombaAdapter/setup.py install

# Requirements

- Python 3.6.x or higher (2.7 is not supported)

- [pyserial](https://pythonhosted.org/pyserial/)

# Documentation

Please check the document for all API and usages.

- [Welcome to PyRoombaAdapter’s documentation\!](https://atsushisakai.github.io/PyRoombaAdapter/)

# Usage examples

All examples are in /exmaples directory.

## Go and back example

```python
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
```


# Contribution

Any contributions to this project are welcome!

Feel free to make an issue and a PR to improve this OSS.

# License

MIT

# Authors

- [Atsushi Sakai](https://github.com/AtsushiSakai/)
