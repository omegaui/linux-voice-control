# run this script to set up master control mode
# you will be asked to speak three times (given only a second)
# speak as much as you can, in your normal tone
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


# records the mic and provides transcription feedback
# @returns: bytes of audio data
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
    elif max(audio_chunks) < 3000:  # no voice in clip
        print('no speech in clip')
        return None
    cprint("transcribing ...", "green", attrs=["bold"])
    cprint(f"You said: {transcribe(dataframes)}", 'blue', attrs=['bold'])
    return dataframes


# saves the audio data and performs and returns the transcription result
# @returns: transcription text from audio data
def transcribe(dataframes):
    WAVE_OUTPUT_FILENAME = 'training-data/internal-transcription.wav'
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(pyAudio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(dataframes))
    wf.close()

    audio_model = whisper.load_model('base.en')  # loading the audio model from whisper
    result = audio_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False, language='english')
    return result['text'].lower().strip()


cprint('\n-----------------------ignore-above-warnings-if-any-----------------------', 'red', attrs=['bold'])
cprint('Welcome to Master Control Mode Setup', "blue", attrs=['bold'])
cprint('We need to record some samples of your voice', "blue", attrs=['bold'])

system_name = config_manager.config['name']
cprint(f'Current System Name: {system_name}', 'blue', attrs=["bold"])
cprint(
    f'Now, you will be asked to speak three times, you can speak whatever you want to trigger your live system, e.g hey {system_name}',
    'green', attrs=['bold'])
cprint('Note: You are given only a second to speak!', 'red', attrs=['bold'])

choice = input('Ready to speak? (y/n) default y: ')
if choice == '':
    choice = 'y'

chances = 3  # no of samples needed

# collecting voice samples ...
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
        cprint('Quitting Master Mode Setup', 'red', attrs=['bold'])
        stream.close()
    if chances == 0:
        break
    choice = input('Ready to speak again? (y/n) default y: ')
    if choice == '':
        choice = 'y'

# creating master data samples ...
if chances != 3:
    cprint('Saving Training Data', 'blue', attrs=['bold'])

    for key in training_data_set:
        frames = b''.join(training_data_set[key])

        wf = wave.open(f'training-data/master_mode_audio_sample{key}.wav', 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyAudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(frames)
        wf.close()

    open('training-data/master-mode', "w").close()

    cprint('Master Mode is all Set!', 'blue', attrs=['bold'])
else:
    cprint('No Training Data collected, restart the program to try again!', 'red', attrs=['bold'])
