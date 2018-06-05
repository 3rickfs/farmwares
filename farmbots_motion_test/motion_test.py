import os
from FARMWARE import MyFarmware
from CeleryPy import log
import sys

if __name__ == "__main__":
    FARMWARE_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '')
    log('Starting the fabulous farmware of ours!', message_type='info', title=FARMWARE_NAME)
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        farmware = MyFarmware(FARMWARE_NAME)
    except Exception as e:
        log(e, message_type='error', title=FARMWARE_NAME + " : init")
        raise Exception(e)
    else:
        try:
            farmware.run()   """Initiate the process"""
        except Exception as e:
            log(e, message_type='error', title=FARMWARE_NAME + " : run")
            raise Exception(e)
    log('Ending our farmware', message_type='info', title=FARMWARE_NAME)

