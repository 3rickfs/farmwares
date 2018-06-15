import os
from FARMWARE import MyFarmware
from CeleryPy import log
import sys

if __name__ == "__main__":
    FARMWARE_NAME = "Motion_test"
    log('Come on, man, just move yourself on', message_type='info', title=FARMWARE_NAME)
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        farmware = MyFarmware(FARMWARE_NAME)
    except Exception as e:
        log(e, message_type='error', title=FARMWARE_NAME + " : init")
        raise Exception(e)
