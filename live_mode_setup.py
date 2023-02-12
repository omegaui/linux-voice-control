# under development
# run this file to set up live mode
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3

import os
import wave
from array import array
from os.path import exists

import pyaudio
import whisper
from termcolor import cprint

import config_manager
from utils import trim

config_manager.init()

# initializing PyAudio ...
pyAudio = pyaudio.PyAudio()

# Opening Microphone Stream with above created configuration ...
stream = pyAudio.open(format=pyaudio.paInt16,
                      channels=2,
                      rate=44100,
                      input=True,
                      frames_per_buffer=1024)

training_data_set = dict()

try:
    if not exists('training-data'):
        os.mkdir('training-data')
except Exception as e:
    print('unable to create training directory')
    exit(1)


def listen():
    dataframes = []
    audio_chunks = array('h')
    cprint("listening ...", "blue", attrs=["bold"])
    for i in range(0, int(44100 / 1024 * 2)):
        data = stream.read(1024)
        dataframes.append(data)  # stacking every audio frame into the list
        audio_chunks.extend(array('h', data))
    audio_chunks = trim(audio_chunks)
    if len(audio_chunks) == 0:  # clip is empty
        print('no voice')
        return None
    elif max(audio_chunks) < 2000:  # no voice in clip
        print('no speech in clip')
        return None
    cprint("transcribing ...", "green", attrs=["bold"])
    cprint(f"You said: {transcribe(dataframes)}", 'blue', attrs=['bold'])
    return dataframes


def transcribe(audioframes):
    WAVE_OUTPUT_FILENAME = 'training-data/internal-transcription.wav'
    waveWriter = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveWriter.setnchannels(2)
    waveWriter.setsampwidth(pyAudio.get_sample_size(pyaudio.paInt16))
    waveWriter.setframerate(44100)
    waveWriter.writeframes(b''.join(audioframes))
    waveWriter.close()

    audio_model = whisper.load_model('base.en')  # loading the audio model from whisper
    result = audio_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False, language='english')
    return result['text'].lower().strip()


cprint('\n-----------------------ignore-above-warnings-if-any-----------------------', 'red', attrs=['bold'])
cprint('Welcome to Live Mode Setup!', 'blue', attrs=['bold'])
cprint('This mode will guide you to setup your control system for instant response.', 'blue', attrs=['bold'])
cprint('Hope! you have reviewed the lvc-config.json file, and your system name is all set.', 'magenta', attrs=['bold'])

system_name = config_manager.config['name']
cprint(f'Current System Name: {system_name}', 'blue', attrs=["bold"])
cprint(f'Now, you will be asked to speak three spawner commands, you can speak whatever you want to trigger your '
       f'live system, e.g hey {system_name}', 'green', attrs=['bold'])
cprint('You are given only a second to speak!', 'red', attrs=['bold'])

choice = input('Ready to say the command? (y/n) default y: ')
if choice == '':
    choice = 'y'

chances = 3

while choice in 'yn':
    if choice == 'y':
        audio_frames = listen()
        if audio_frames is not None:
            chx = input('Record again or save? (y/n) default y: ')
            if chx == '':
                chx = 'y'
            if chx == 'y':
                cprint('>>> Saved!', 'green', attrs=['bold'])
                training_data_set[chances] = audio_frames
                chances -= 1
        else:
            cprint('Try Again!', 'blue', attrs=['bold'])
    else:
        cprint('Quitting Live Mode Setup', 'red', attrs=['bold'])
        stream.close()
    if chances == 0:
        break
    choice = input('Ready to say the next command? (y/n) default y: ')
    if choice == '':
        choice = 'y'

def compare(key1, key2):
    # Load the audio files
    import librosa
    y1, sr1 = librosa.load(f'training-data/live_mode_training_audio{key1}.wav')
    y2, sr2 = librosa.load(f'training-data/live_mode_training_audio{key2}.wav')

    # Extract MFCCs from the audio files
    mfccs1 = librosa.feature.mfcc(y=y1, sr=sr1)
    mfccs2 = librosa.feature.mfcc(y=y2, sr=sr2)

    # Calculate the Euclidean distance between the MFCCs
    import numpy as np
    distance = np.linalg.norm(mfccs1 - mfccs2)

    return distance

# creating live data file ...
if chances != 3:
    cprint('Saving Training Data', 'blue', attrs=['bold'])

    for key in training_data_set:
        frames = b''.join(training_data_set[key])

        wf = wave.open(f'training-data/live_mode_training_audio{key}.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyAudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(frames)
        wf.close()

    cprint('performing some calculations ...', 'blue')

    distance1 = compare(1, 2)
    distance2 = compare(2, 3)
    distance3 = compare(3, 1)

    highestPossibleDistance = max(distance1, distance2, distance3)

    file = open(f'training-data/live_mode_data', 'w')
    file.write(f"max-euclidean-distance={highestPossibleDistance}")
    file.close()

    cprint('Live Mode is all Set!', 'blue', attrs=['bold'])
else:
    cprint('No Training Data collected, restart the program to try again!', 'red', attrs=['bold'])
