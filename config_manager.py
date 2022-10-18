# the command management system, manages configurations.
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import json
import os
from notifier import notify

# stores the configuration from the lvc-config.json
config = dict()


# initializing config with configuration specified in lvc-config.json
def init():
    global config
    config = get_config_from_file()
    validate_config()


# getting json data from file
def get_config_from_file():
    return json.load(open(os.path.join(os.getcwd(), "lvc-config.json")))


# validating the configuration received from lvc-config.json
def validate_config():
    notify("📢 config-error: ~/lvc-bin/lvc-config.json has errors.")
    if config['name'] == '':
        raise Exception("📢 config-error: name field of the voice-control-system cannot be null")
    if config['record-duration'] <= 0:
        raise Exception("📢 config-error: record-duration must be greater than zero")
