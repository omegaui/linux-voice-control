import json
from array import array

import pyaudio
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

# creating live data file ...
file = open('live_data.lvc', 'w')
training_data_set = dict()


def listen():
    frames = []
    audio_chunks = array('h')
    cprint("listening ...", "blue", attrs=["bold"])
    for i in range(0, int(44100 / 1024 * 2)):
        data = stream.read(1024)
        frames.append(data)  # stacking every audio frame into the list
        audio_chunks.extend(array('h', data))
    audio_chunks = trim(audio_chunks)
    if len(audio_chunks) == 0:  # clip is empty
        print('no voice')
        return None
    elif max(audio_chunks) < 3000:  # no voice in clip
        print('no speech in clip')
        return None
    return audio_chunks


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
        chunk_array = listen()
        if chunk_array is not None:
            training_data_set[chances] = chunk_array.tolist()
            chances -= 1
        else:
            cprint('Try Again!', 'blue', attrs=['bold'])
    else:
        cprint('Quitting Live Mode Setup', 'red', attrs=['bold'])
        stream.close()
    if chances == 0:
        break
    choice = 'y'
    choice = input('Ready to say the next command? (y/n) default y: ')
    if choice == '':
        choice = 'y'

if chances != 3:
    cprint('Saving Training Data', 'blue', attrs=['bold'])
    cprint('Live Mode is all Set!', 'blue', attrs=['bold'])
    file.write(json.dumps(training_data_set))
else:
    cprint('No Training Data collected, restart the program to try again!', 'red', attrs=['bold'])
file.close()
