# shows desktop notifications
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import os
import subprocess

import config_manager

username = os.environ.get("USERNAME")


# Sends a Desktop Notification using notify-send command
def notify(message, duration=0):
    if not config_manager.config['notifications-enabled']:
        return
    subprocess.call(
        ['notify-send', f'--icon=/home/{username}/lvc-bin/lvc-icon.png', '--app-name=\"Linux Voice Control\"', f'--expire-time={duration}', "--transient", "Linux Voice Control", message])
