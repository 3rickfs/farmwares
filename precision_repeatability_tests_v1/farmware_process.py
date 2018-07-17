import os
from API import API
from CeleryPy import log
from CeleryPy import move_absolute
from plant_detection.Image import Image
from plant_detection.Parameters import Parameters
from plant_detection.DB import DB
from plant_detection import ENV
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from plant_detection.PlantDetection import PlantDetection
from time import gmtime, strftime, time
import json
import requests
import numpy as np
import cv2


class MyFarmware():
    def __init__(self, farmwarename):
        self.farmwarename = farmwarename
        prefix = self.farmwarename.lower().replace('-', '_')
        self.input_default_speed = int(os.environ.get(prefix + "_default_speed", 800))
        self.x_photo_pos = 400
        self.y_photo_pos = 235
        self.z_photo_pos = 0
        self.image = None
        self.plant_db = DB()
        self.params = Parameters()
        self.plant_detection = None

        """"self.api = API(self)
        self.points = []"""
    def mov_robot_origin(self):
        log('Execute move: ', message_type='debug', title=str(self.farmwarename))
        move_absolute(
            location=[0, 0, 0],
            offset=[0, 0, 0],
            speed=800)
    def mov_robot_photo(self):
        log('Execute move: ', message_type='debug', title=str(self.farmwarename))
        move_absolute(
            location=[self.x_photo_pos, self.y_photo_pos, self.z_photo_pos],
            offset=[0, 0, 0],
            speed=800)
    def take_photo(self):
        self.image = Image(self.params, self.plant_db)
        self.image.capture()
        self.image.save('Seedling_photo_' + strftime("%Y-%m-%d_%H:%M:%S", gmtime()))

    def process_photo(self):
        self.plant_detection = PlantDetection(coordinates=True, app=True)
        self.plant_detection.detect_plan()
    """def graph_plant_centroid(self):

    def execute_sequence_init(self):"""

    def save_data(self, idata):
        HEADERS = {
            'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
            'content-type': 'application/json'}

        def timestamp(value):
            """Add a timestamp to the pin value."""
            return {'time': time(), 'value': value}

        def append(data):
            """Add new data to existing data."""
            try:
                existing_data = json.loads(os.environ[LOCAL_STORE])
            except KeyError:
                existing_data = []
            existing_data.append(data)
            return existing_data

        def wrap(data):
            """Wrap the data in a `set_user_env` Celery Script command to save it."""
            return {
                'kind': 'set_user_env',
                'args': {},
                'body': [{
                    'kind': 'pair',
                    'args': {
                        'label': LOCAL_STORE,
                        'value': json.dumps(data)
                    }}]}

        def post(wrapped_data):
            """Send the Celery Script command."""
            payload = json.dumps(wrapped_data)
            requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                          data=payload, headers=HEADERS)
            log('Data is supposed to be saved')

        LOCAL_STORE = 'test_data'
        post(wrap(append(timestamp(idata))))

    def plot_data(self):
        TIME_SCALE_FACTOR = 60 * 2
        DATA_SCALE_FACTOR = 2
        RECENT = {'time': None}

        def post(wrapped_data):
            """Send the Celery Script command."""
            headers = {
                'Authorization': 'bearer {}'.format(os.environ['FARMWARE_TOKEN']),
                'content-type': 'application/json'}
            payload = json.dumps(wrapped_data)
            requests.post(os.environ['FARMWARE_URL'] + 'api/v1/celery_script',
                          data=payload, headers=headers)

        def no_data_error():
            """Send an error to the log if there's no data."""
            message = 'No data available'
            wrapped_message = {
                'kind': 'send_message',
                'args': {
                    'message_type': 'error',
                    'message': message}}
            post(wrapped_message)

        def get_data():
            """Get existing historical pin data."""
            data = json.loads(os.getenv('test_data', '[]'))
            if len(data) < 1:
                no_data_error()
                sys.exit(0)
            else:
                return data

        def reduce_data(data):
            """Reduce the loaded data for plotting."""
            times, values = [], []
            for record in data:
                times.append(round(float(record['time']) / TIME_SCALE_FACTOR))
                values.append(round(float(record['value']) / DATA_SCALE_FACTOR))
            RECENT['time'] = max(times) * TIME_SCALE_FACTOR
            times = abs(np.array(times) - max(times))
            all_data = np.column_stack((times, values))
            filtered_data = all_data[all_data[:, 0] < 720]
            return filtered_data

        def plot(data):
            """Plot the reduced data."""
            # Create blank plot
            p = np.full([512, 24 * 60 / 2], 255, np.uint8)
            # Add shaded plot areas
            for i in range(512):
                if i < 100:  # N/A
                    p[i, :] = 220
                elif i > 425:  # off
                    p[i, :] = 220
                else:  # sensor range (gradient)
                    p[i, :] = 255 - 175 * ((i - 100) / float(425 - 100))
            # Add horizontal gridlines
            for i in range(0, 512, 32):
                p[i, :] = 100
                if i == 384:
                    p[i, :] = 125
            # Add minor vertical gridlines
            for i in range(0, 720, 30):
                p[:, i] = 100
            # Add major vertical gridlines
            for i in range(0, 720, 90):
                p[:, i - 1:i + 1] = 100
            # Add plot border
            cv2.rectangle(p, (0, 0), (719, 511), 50, 4)
            # Add data
            for record in data:
                reading_time = int(record[0])
                reading_value = int(record[1])
                cv2.circle(p, (reading_time, reading_value), 5, 0, 3)
            # Flip plot to display oldest to newest, low to high
            p = cv2.flip(p, -1)
            # Create plot border label area
            border = np.full([800, 600], 255, np.uint8)

            def _add_labels(image_area, labels):
                for label in labels:
                    cv2.putText(image_area, label['text'].upper(),
                                label['position'], 0, 0.5, 0, 1)

            # Add sensor range text
            """range_labels = [{'text': 'off', 'position': (500, 25)},
                            {'text': 'wet', 'position': (425, 25)},
                            {'text': 'dry', 'position': (160, 25)},
                            {'text': 'n/a', 'position': (75, 25)}]

            _add_labels(border, range_labels)"""
            # Flip labels to display vertically
            full = cv2.flip(cv2.transpose(border), 0)
            # Add sensor value labels
            value_labels = [{'text': '0', 'position': (760, 560)},
                            {'text': '512', 'position': (760, 305)},
                            {'text': '1023', 'position': (760, 50)}]
            _add_labels(full, value_labels)
            # Add most recent time
            time_string = strftime('%b %d %H:%M UTC', gmtime(RECENT['time']))
            _add_labels(full, [{'text': time_string, 'position': (650, 580)}])
            # Add time offset labels
            for i, column in enumerate(range(10, 600, 90)[::-1]):
                _add_labels(full, [{'text': '-{} hr'.format(6 + i * 3),
                                    'position': (column, 580)}])
            # Add label area to plot area
            full[44:556, 40:760] = p
            # Add plot title
            title = 'Database tests'
            cv2.putText(full, title.upper(), (325, 25), 0, 0.75, 0, 2)
            return full

        def save(image):
            """Save the plot image."""
            filename = '/test_data_plot_{}.png'.format(int(time()))
            log('Image to be saved in: ' + os.environ['IMAGES_DIR'] + filename)
            cv2.imwrite(os.environ['IMAGES_DIR'] + filename, image)

        """PIN = get_env('pin')
        IS_SOIL_SENSOR = PIN == 59"""
        save(plot(reduce_data(get_data())))

    #def save_data(self):

    def run(self):
        self.mov_robot_origin()
        self.mov_robot_photo()
        #self.take_photo()
        #self.process_photo()
        for i in range(0, 500, 21):
            self.save_data(i)
        self.plot_data()
        sys.exit(0)
