import os
from FARMWARE import MyFarmware
from CeleryPy import log
import sys

if __name__ == "__main__":
    FARMWARE_NAME = "precision_repeatability_test_v1"
    log('Experiments to know robots precision and repeatability', message_type='info', title=FARMWARE_NAME)
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        farmware = MyFarmware(FARMWARE_NAME)
    except Exception as e:
        log(e, message_type='error', title=FARMWARE_NAME + " : init")
        raise Exception(e)
    else:
        try:
            farmware.run()
        except Exception as e:
            log(e,message_type='error', title=FARMWARE_NAME + " : run")
raise Exception(e)