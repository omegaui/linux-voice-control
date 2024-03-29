# uses gTTS to provide voice feedback
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import os.path
import random
import sys

import mpv
from gtts import gTTS, gTTSError
from termcolor import cprint

import config_manager
import notifier

internet = False

wroteLiveModeSpeech = False
wroteExecutionSpeech = False
wroteExitingSpeech = False
wroteTranscriptionSpeech = False

player = None
try:
    player = mpv.MPV(ytdl=True)  # using mpv
except Exception:
    cprint("voice feedback requires mpv media player installed on your distro!", "red")


# initialized voice control to check network state
def init():
    global internet
    internet = check_network()


# handling voice feedback
def speak(text, wait=False):
    if not config_manager.config['voice-feedback-enabled']:
        return
    player.speed = config_manager.config['voice-feedback-speed']
    try:
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save('misc/last-feedback-speech.mp3')
        player.play('misc/last-feedback-speech.mp3')
        if wait:
            player.wait_for_playback()
        return speech
    except gTTSError as e:
        if str(e).find('Failed to connect') >= 0:
            player.play('misc/network-error.mp3')
            player.wait_for_playback()
            print("📢 Network connection is required for voice feedback!", file=sys.stderr)
        else:
            player.play('misc/internal-voice-feedback-error.mp3')
            player.wait_for_playback()
            config_manager.config['voice-feedback-enabled'] = False
            notifier.notify('Voice-Feedback failed, See logs!', force=True)
            print(e)


# internal function to create default voice feedbacks
def _speak_and_save(text, filename):
    player.speed = config_manager.config['voice-feedback-speed']
    try:
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save(filename)
    except gTTSError as ex:
        print(ex)


# voice feedback when a command is executed
def give_execution_feedback():
    if len(config_manager.config['voice-feedback-default-speeches']) == 0:
        return
    global wroteExecutionSpeech
    if internet and not wroteExecutionSpeech:
        speech = speak(random.choice(config_manager.config['voice-feedback-default-speeches']), wait=True)
        if config_manager.config['voice-cache-enabled']:
            speech.save('misc/execution-feedback.mp3')
            wroteExecutionSpeech = True
    elif os.path.exists('misc/execution-feedback.mp3'):
        player.speed = config_manager.config['voice-feedback-speed']
        player.play('misc/execution-feedback.mp3')
        player.wait_for_playback()


# voice feedback when exiting
def give_exiting_feedback():
    global wroteExitingSpeech
    if internet and not wroteExitingSpeech:
        speech = speak(config_manager.config['voice-feedback-turning-off'], wait=True)
        if config_manager.config['voice-cache-enabled']:
            speech.save('misc/exiting-feedback.mp3')
            wroteExitingSpeech = True
    elif os.path.exists('misc/exiting-feedback.mp3'):
        player.speed = config_manager.config['voice-feedback-speed']
        player.play('misc/exiting-feedback.mp3')
        player.wait_for_playback()

# voice feedback when initializing live mode
def give_live_mode_feedback():
    global wroteLiveModeSpeech
    if internet and not wroteLiveModeSpeech:
        speech = speak("voice control is running in live mode.", wait=False)
        if config_manager.config['voice-cache-enabled']:
            speech.save('misc/live_mode-feedback.mp3')
            wroteLiveModeSpeech = True
    elif os.path.exists('misc/live_mode-feedback.mp3'):
        player.speed = config_manager.config['voice-feedback-speed']
        player.play('misc/live_mode-feedback.mp3')


# required for live voice control
def give_transcription_feedback():
    if len(config_manager.config['voice-feedback-transcription-capable-speeches']) == 0:
        return
    global wroteTranscriptionSpeech
    if config_manager.config['voice-transcription-feedback-enabled']:
        if internet and not wroteTranscriptionSpeech:
            speech = speak(random.choice(config_manager.config['voice-feedback-transcription-capable-speeches']))
            if config_manager.config['voice-cache-enabled']:
                speech.save('misc/transcription-feedback.mp3')
                wroteTranscriptionSpeech = True
        elif os.path.exists('misc/transcription-feedback.mp3'):
            player.speed = config_manager.config['voice-feedback-speed']
            player.play('misc/transcription-feedback.mp3')


# checks if network is reachable
def check_network():
    try:
        gTTS(text='checking network connectivity ...', lang='en', slow=False).save('misc/network-test.mp3')
        return True
    except gTTSError:
        return False


# voice greeting
def greet():
    if internet:
        speech = speak(config_manager.config['greeting'], wait=True)
        if config_manager.config['voice-cache-enabled']:
            speech.save('misc/greeting.mp3')
    else:
        player.speed = config_manager.config['voice-feedback-speed']
        player.play('misc/greeting.mp3')
        player.wait_for_playback()


# generates and saves default voice feedbacks
# network-error-feedback
# internal-exception-feedback
def gen_default_speeches():
    _speak_and_save('Connect to a network to use voice feedback.', 'misc/network-error.mp3')
    _speak_and_save(
        'Some internal error occurred in the voice feedback system, turning off voice feedback for this session!',
        'misc/internal-voice-feedback-error.mp3')
