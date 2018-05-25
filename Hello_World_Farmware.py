import os
import json
import requests


def api_url():
    major_version = int(os.getenv('FARMBOT_OS_VERSION', '0.0.0')[0])
    base_url = os.environ['FARMWARE_URL']
    return base_url + 'api/v1/' if major_version > 5 else base_url


def post(wrapped_data):
    """Send the Celery Script command"""
    headers = {
        'Authorization': 'bearer{}'.format(os.environ['FARMWARE_TOKEN']),
        'content-type': "application/json"}
    payload = json.dumps(wrapped_data)
    requests.post(api_url() + 'celery_script',
                  data=payload, headers=headers)


def print_message(message):
    """Function to sed messages from a python program"""
    wrapped_message = {
        "kind": "send_message",
        "args": {
            "message_type": "alert",
            "message": message}}
    post(wrapped_message)


if __name__ == "__main__":
    print_message("Hey you I'm greeting you from a python code!")

