import numpy as np
from thorlabs_elliptec import ELLx, ELLError, ELLStatus, list_devices
import redpitaya_scpi as scpi
import time

class calibration:
    def __init__(self):
        self.x = 0 