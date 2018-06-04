#!/usr/bin/env python
import os
from CeleryPy import log
import sys

if __name__ == "__main__":
    FARMWARE_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '')
    log('Start... hello world!', message_type='info', title=FARMWARE_NAME)
    sys.setdefaultencoding('utf8')
