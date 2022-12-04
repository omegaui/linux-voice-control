# the command management system, manages configurations.
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import json
import os

# stores the configuration from the lvc-config.json
config = dict()
live_config = dict()


# initializing config with configuration specified in lvc-config.json
def init():
    global config, live_config
    config = get_config_from_file("lvc-config.json")
    live_config = get_config_from_file("live_data.json")
    validate_config()


# getting json data from file
def get_config_from_file(filename):
    try:
        return json.load(open(os.path.join(os.getcwd(), filename)))
    except Exception as e:
        return dict()


# validating the configuration received from lvc-config.json
def validate_config():
    if config['name'] == '':
        raise Exception("📢 config-error: name field of the voice-control-system cannot be null")
    if config['record-duration'] <= 0:
        raise Exception("📢 config-error: record-duration must be greater than zero")
    if config['record-duration'] <= 0:
        raise Exception("📢 config-error: record-duration must be greater than zero")
