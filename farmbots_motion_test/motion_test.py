import os
from FARMWARE import MyFarmware
from CeleryPy import log
import sys

if __name__ == "__main__":
    FARMWARE_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '')
    log(FARMWARE_NAME)
