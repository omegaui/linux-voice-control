# the entry point of this excellent voice control program
# we are in public preview still.
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3
import wave

import click
import pyaudio
import whisper
from termcolor import cprint

import command_manager
import config_manager


@click.command()
@click.option("--model", default="base", help="Model to use",
              type=click.Choice(["tiny", "base", "small", "medium", "large"]))
def main(model='base'):
    """
    the main function ... everything begins from here :param model: default model used is "base" from the available
    models in whisper ["tiny", "base", "small", "medium", "large"]
    """
    model = model + ".en"  # default langauge is set to english, you can change this anytime just refer to whisper docs
    audio_model = whisper.load_model(model)  # loading the audio model from whisper

    # initializing configuration management ...
    config_manager.init()

    # getting configurations from lvc-config.json file ...
    CHUNK = config_manager.config['chunk-size']  # getting the chunk size configuration
    FORMAT = pyaudio.paInt16
    CHANNELS = config_manager.config['channels']  # getting the number of channels from configuration
    RATE = config_manager.config['rate']  # getting the frequency configuration
    RECORD_SECONDS = config_manager.config['record-duration']  # getting the record duration
    WAVE_OUTPUT_FILENAME = "lvc-last-mic-fetch.wav"  # default file which will be overwritten in every RECORD_SECONDS

    # initializing PyAudio ...
    p = pyaudio.PyAudio()

    # Opening Microphone Stream with above created configuration ...
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    cprint("🐧 loading commands file ...", "blue")
    # initializing command management ...
    command_manager.init()

    cprint(f'🚀 voice control ready ... listening every {RECORD_SECONDS} seconds', "blue")

    name = config_manager.config['name']
    cprint(f'{name} waiting for order ...', "cyan")

    # And here it begins
    while True:
        frames = []
        cprint("listening ...", "blue", attrs=["bold"])
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)  # stacking every audio frame into the list
        print("saving audio ...")

        # writing the wave file
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("transcribing audio data ...")
        # transcribing audio ...
        # fp16 isn't supported on every CPU using,
        # fp32 by default.
        result = audio_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False)

        cprint("analyzing results ...", "magenta", attrs=["bold"])
        # analyzing results ...
        analyze_text(result["text"].lower().strip())


def analyze_text(text):
    # validating transcribed text ...
    if text == '':
        return  # no speech data available returning without performing any operation

    cprint(f'You: {text}', "blue", attrs=["bold"])

    if text[len(text) - 1] in " .!?":
        text = text[0:len(text) - 1]  # removing any punctuation from the transcribed text

    # and here comes the command manager
    # it checks for suitable match of transcribed text against the available commands from the lvc-commands.json file
    command_manager.launch_if_any(text)


# spawning the process
main()
