import random
import sys

import mpv
from gtts import gTTS, gTTSError
from termcolor import cprint

import config_manager
import notifier

player = None
try:
    player = mpv.MPV(ytdl=True)  # using mpv
except Exception as e:
    cprint("voice feedback requires mpv media player installed on your distro!", "red")


# handling voice feedback
def speak(text, wait=False):
    if not config_manager.config['voice-feedback-enabled']:
        return
    try:
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save('last-feedback-speech.mp3')
        player.speed = config_manager.config['voice-feedback-speed']
        player.play('last-feedback-speech.mp3')
        if wait:
            player.wait_for_playback()
    except gTTSError as e:
        if str(e).find('Failed to connect') >= 0:
            notifier.notify('Voice Feedback requires network connection!')
            print("📢 Network connection is required for voice feedback!", file=sys.stderr)
        else:
            notifier.notify('Voice Feedback failed, See logs!')
            print(e)


# voice feedback when a command is executed
def giveexecutionfeedback():
    speak(random.choice(config_manager.config['voice-feedback-default-speeches']), wait=True)


# required for live voice control -- TODO
def givetranscribingfeedback():
    if config_manager.config['voice-transcription-feedback-enabled']:
        speak(random.choice(config_manager.config['voice-feedback-transcription-capable-speeches']), wait=True)
