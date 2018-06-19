import os
import datetime
from API import API
from CeleryPy import log
from CeleryPy import move_absolute
from CeleryPy import execute_sequence
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from plant_detection.PlantDetection import PlantDetection

class MyFarmware():

    def __init__(self,farmwarename):
        self.farmwarename = farmwarename
        prefix = self.farmwarename.lower().replace('-', '_')
        self.input_default_speed = int(os.environ.get(prefix + "_default_speed", 800))
        """"self.api = API(self)
        self.points = []"""
    
    def execute_sequence_init(self):
        log('Execute move: ', message_type= 'debug', title=str(self.farmwarename))
        move_absolute(
            location=[400,100,0],
            offset=[0,0,0],
            speed=800)   
        PD = PlantDetection(coordinates=True, app=True)
        PD.detect_plants()

    def run(self):
        self.execute_sequence_init()
