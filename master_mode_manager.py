from speechbrain.pretrained import SpeakerRecognition


# uses speechbrain to check if the current mic fetched audio is same as the master mode sample audio
def isMasterSpeaking():
    verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                                   savedir="pretrained_models/spkrec-ecapa-voxceleb")
    for i in range(1, 4):
        score, prediction = verification.verify_files(f"training-data/master_mode_audio_sample{i}.wav",
                                                      "misc/last-mic-fetch.wav")
        if not not prediction[0]:
            return True
    return False
