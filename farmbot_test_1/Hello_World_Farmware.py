#!/usr/bin/env python
import os
from CeleryPy import log

if __name__ == "__main__":
    FARMWARE_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '')
    log('Starting the fabulous farmware of ours!', message_type='info', title=FARMWARE_NAME)


