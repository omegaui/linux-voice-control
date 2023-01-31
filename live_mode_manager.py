# under development
# live mode manager
# author: @omegaui
# github: https://github.com/omegaui/linux-voice-control
# license: GNU GPL v3


import librosa
import numpy as np

# stores the maximum euclidean distance among live mode samples
threshold = -1

# stores the data and the samplerate of the live mode samples
# e.g: [(y1, sr1), ...]
trainingDataSet = []

# reads and stores live mode samples and threshold
def init():
    global threshold

    signal1, samplerate1 = librosa.load('training-data/live_mode_training_audio1.wav')
    signal2, samplerate2 = librosa.load('training-data/live_mode_training_audio2.wav')
    signal3, samplerate3 = librosa.load('training-data/live_mode_training_audio3.wav')
    trainingDataSet.append((signal1, samplerate1))
    trainingDataSet.append((signal2, samplerate2))
    trainingDataSet.append((signal3, samplerate3))

    file = open('training-data/live_mode_data')
    text = file.read()
    threshold = float(text[text.find('=') + 1:])
    file.close()

# compares two mfccs and return the euclidean distance between them
def compareWith(y1, sr1, y2, sr2):

    # Extract MFCCs from the audio files
    mfccs1 = librosa.feature.mfcc(y=y1, sr=sr1)
    mfccs2 = librosa.feature.mfcc(y=y2, sr=sr2)

    # Calculate the Euclidean distance between the MFCCs
    distance = np.linalg.norm(mfccs1 - mfccs2)

    return distance


# compares the speech with live samples to find the minimum closest relative
# return True if speech matches with any of the live samples
def compare():
    y1, sr1 = librosa.load('training-data/live-speech-data.wav')

    d1 = compareWith(y1, sr1, trainingDataSet[0][0], trainingDataSet[0][1])
    d2 = compareWith(y1, sr1, trainingDataSet[1][0], trainingDataSet[1][1])
    d3 = compareWith(y1, sr1, trainingDataSet[2][0], trainingDataSet[2][1])

    distance = min(d1, d2, d3)

    print(distance)

    return distance <= threshold

