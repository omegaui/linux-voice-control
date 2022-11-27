import random

import mpv
from gtts import gTTS
from termcolor import cprint

import config_manager

player = None
try:
    player = mpv.MPV(ytdl=True)  # using mpv
except Exception as e:
    cprint("voice feedback requires mpv media player installed on your distro!", "red")


# handling voice feedback
def speak(text, wait=False):
    if not config_manager.config['voice-feedback-enabled']:
        return
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save('last-feedback-speech.mp3')
    player.speed = config_manager.config['voice-feedback-speed']
    player.play('last-feedback-speech.mp3')
    if wait:
        player.wait_for_playback()


def givedefaultfeedback():
    speak(getrandomdefaultfeeback())


def getrandomdefaultfeeback():
    speeches = config_manager.config['voice-feedback-default-speeches']
    value = random.randint(0, len(speeches) - 1)
    return speeches[value]
