import wave

import click
import pyaudio
import whisper

import command_manager
import config_manager


@click.command()
@click.option("--model", default="base", help="Model to use",
              type=click.Choice(["tiny", "base", "small", "medium", "large"]))
def main(model='base'):
    model = model + ".en"
    audio_model = whisper.load_model(model)

    config_manager.init()

    CHUNK = config_manager.config['chunk-size']
    FORMAT = pyaudio.paInt16
    CHANNELS = config_manager.config['channels']
    RATE = config_manager.config['rate']
    RECORD_SECONDS = config_manager.config['record-duration']
    WAVE_OUTPUT_FILENAME = "lvc-last-mic-fetch.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🐧 loading commands file ...")
    command_manager.init()

    print("🚀 voice control ready ... listening every", RECORD_SECONDS, "seconds")
    print(config_manager.config['name'], "waiting for order ...")
    while True:
        frames = []
        # get and save audio to wav file
        print("listening ...")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("saving audio ...")

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("transcribing audio data ...")
        result = audio_model.transcribe(WAVE_OUTPUT_FILENAME, fp16=False)

        analyze_text(result["text"].lower().strip())


def analyze_text(text):
    if text == '':
        return
    print("You:", text)
    if text[len(text) - 1] in " .!?":
        text = text[0:len(text) - 1]

    command_manager.launch_if_any(text)


main()
