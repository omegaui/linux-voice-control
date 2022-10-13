import json
import os

config = dict()


def init():
    global config
    config = get_config_from_file()
    validate_config()


def get_config_from_file():
    return json.load(open(os.path.join(os.getcwd(), "lvc-config.json")))


def validate_config():
    if config['name'] == '':
        raise Exception("📢 config-error: name field of the voice-control-system cannot be null")
    if config['record-duration'] <= 0:
        raise Exception("📢 config-error: record-duration must be greater than zero")
