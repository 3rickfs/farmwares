import os
import datetime
from API import API
from CeleryPy import log
from CeleryPy import move_absolute
from CeleryPy import execute_sequence

class MyFarmware():

    def __init__(self,farmwarename):
        self.farmwarename = farmwarename
        prefix = self.farmwarename.lower().replace('-', '_')
        """self.get_input_env()"""
        self.input_default_speed = int(os.environ.get(prefix + "_default_speed", 800))
        self.api = API(self)
        self.points = []


    def check_celerypy(self,ret):
        try:
            status_code = ret.status_code
        except:
            status_code = -1
        try:
            text = ret.text[:100]
        except expression as identifier:
            text = ret
        if status_code == -1 or status_code == 200:
            if self.input_debug >= 1: log("{} -> {}".format(status_code,text), message_type='debug', title=self.farmwarename + ' check_celerypy')
        else:
            log("{} -> {}".format(status_code,text), message_type='error', title=self.farmwarename + ' check_celerypy')
            raise

    
    def execute_sequence_init(self):
        log('Execute move: ', message_type= 'debug', title=str(self.farmwarename))
        self.check_celerypy(move_absolute(
            location=[100,100,0],
            offset=[0,0,0],
            speed=800))


    def save_meta(self,point):
        if str(self.input_save_meta_key).lower() != 'none':
            if self.input_debug >= 1: log('Save Meta Information: ' + str(point['id']) , message_type='debug', title=str(self.farmwarename) + ' : save_meta')
            if self.input_debug < 2 :
                point['meta'][self.input_save_meta_key]=self.input_save_meta_value
                endpoint = 'points/{}'.format(point['id'])
                self.api.api_put(endpoint=endpoint, data=point)
    
    
    def run(self):
        self.execute_sequence_init()
