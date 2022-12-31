# the entry point of this excellent voice control program
# we are in public preview still.
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3
import os
import sys
import wave
from array import array
from os.path import exists

import click
import pyaudio
import whisper
from termcolor import cprint

import command_manager
import config_manager
import live_mode_manager
import voice_feedback
from master_mode_manager import isMasterSpeaking
from utils import trim

try:
    if not exists('misc'):
        os.mkdir('misc')
except Exception as e:
    print('unable to create training directory')
    exit(1)


def log(text, color=None, attrs=None):
    if attrs is None:
        attrs = []
    if color is None:
        print(text)
    elif config_manager.config['logs']:
        cprint(text, color, attrs=attrs)


@click.command()
@click.option("--model", default="base", help="Model to use",
              type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--ui", default="false", help="Launch in UI Mode [true/false]",
              type=click.Choice(["true", "false"]))
def main(model='base', ui='false'):
    """
    the main function ... everything begins from here :param model: default model used is "base" from the available
    models in whisper ["tiny", "base", "small", "medium", "large"]
    """
    if ui == 'true':
        sys.stdout = sys.stderr

    # initializing configuration management ...
    config_manager.init()

    # greeting ...
    voice_feedback.init()
    voice_feedback.greet()

    model = model + ".en"  # default langauge is set to english, you can change this anytime just refer to whisper docs
    audio_model = whisper.load_model(model)  # loading the audio model from whisper

    # getting configurations from lvc-config.json file ...
    CHUNK = config_manager.config['chunk-size']  # getting the chunk size configuration
    FORMAT = pyaudio.paInt16
    CHANNELS = config_manager.config['channels']  # getting the number of channels from configuration
    RATE = config_manager.config['rate']  # getting the frequency configuration
    RECORD_SECONDS = config_manager.config['record-duration']  # getting the record duration
    WAVE_OUTPUT_FILENAME = "misc/last-mic-fetch.wav"  # default file which will be overwritten in every RECORD_SECONDS
    SPEECH_THRESHOLD = config_manager.config['speech-threshold']  # speech threshold default 4000 Hz

    # initializing PyAudio ...
    pyAudio = pyaudio.PyAudio()

    # Opening Microphone Stream with above created configuration ...
    stream = pyAudio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

    log("🐧 loading commands file ...", "blue")

    # initializing command management ...
    command_manager.init()

    log(f'🚀 voice control ready ... listening every {RECORD_SECONDS} seconds', "blue")

    name = config_manager.config['name']
    log(f'{name} waiting for order ...', "cyan")

    # validating master mode ...
    if config_manager.config['master-mode']:
        enabled = os.path.exists('training-data/master-mode')
        if enabled:
            log(f'MASTER CONTROL MODE: ON', "blue", attrs=['bold'])
            voice_feedback.speak('Activating Master Control Mode, listening ...', wait=True)
        else:
            config_manager.config['master-mode'] = False
            voice_feedback.speak('You need to run master control mode setup to use this mode!', wait=True)
            voice_feedback.speak('Turning off master control mode for this session!', wait=True)
            log(f'Run master control mode setup before using it!', "red", attrs=['bold'])
            log(f'Turning MASTER CONTROL MODE: OFF', "red", attrs=['bold'])

    # well, this is under development,
    # I don't recommend activating live mode until it is ready!
    if config_manager.config['live-mode']:
        live_mode_manager.init()
        while True:
            frames = []
            chunk_array = array('h')
            log("listening ...", "blue", attrs=["bold"])
            for i in range(0, int(44100 / 1024 * 2)):
                data = stream.read(1024)
                frames.append(data)  # stacking every audio frame into the list
                chunk_array.extend(array('h', data))
            chunk_array = trim(chunk_array)
            if len(chunk_array) == 0:  # clip is empty
                log('no voice')
                continue
            elif max(chunk_array) < SPEECH_THRESHOLD:  # no voice in clip
                log('no speech in clip')
                continue
            log("saving ...")

            # writing the wave file
            wf = wave.open('training-data/live-speech-data.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyAudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            log("comparing ...", "blue", attrs=["bold"])
            if live_mode_manager.compare():
                voice_feedback.speak('yes sir!', wait=True)
                exit(0)
            else:
                voice_feedback.speak('match test failed!', wait=True)

            frames.clear()
    else:
        # And here begins the manual mode
        while True:
            frames = []
            chunk_array = array('h')
            log("listening ...", "blue", attrs=["bold"])
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)  # stacking every audio frame into the list
                chunk_array.extend(array('h', data))
            chunk_array = trim(chunk_array)
            if len(chunk_array) == 0:  # clip is empty
                log('no voice')
                continue
            elif max(chunk_array) < SPEECH_THRESHOLD:  # no voice in clip
                log('no speech in clip')
                continue
            print("saving audio ...")

            # writing the wave file
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyAudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # checking if master control mode is enabled
            # and performing audio analysis if enabled
            if config_manager.config['master-mode']:
                log('performing master mode analysis ...', "green", attrs=['bold'])
                if not isMasterSpeaking():
                    log('performing master mode analysis ... failed', "red", attrs=['bold'])
                    if config_manager.config['master-mode-barrier-speech-enabled']:
                        voice_feedback.speak(config_manager.config['master-mode-barrier-speech'], wait=True)
                    continue
                log('performing master mode analysis ... succeeded', "green", attrs=['bold'])
            voice_feedback.give_transcription_feedback()
            log("transcribing audio data ...")
            # transcribing audio ...
            # fp16 isn't supported on every CPU using,
            # fp32 by default.
            result = audio_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False, language='english')

            log("analyzing results ...", "magenta", attrs=["bold"])
            # analyzing results ...
            analyze_text(result["text"].lower().strip())

            frames.clear()


def analyze_text(text):
    # validating transcribed text ...
    if text == '':
        return  # no speech data available returning without performing any operation

    log(f'You: {text}', "blue", attrs=["bold"])

    if text[len(text) - 1] in " .!?":
        text = text[0:len(text) - 1]  # removing any punctuation from the transcribed text

    # and here comes the command manager
    # it checks for suitable match of transcribed text against the available commands from the lvc-commands.json file
    command_manager.launch_if_any(text)


# spawning the process
main()
