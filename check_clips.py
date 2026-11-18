# check_clips.py
# Lists every .wav clip in data/sample_audio with its length and any problems.

import os

import stt

for name in sorted(os.listdir("data/sample_audio")):
    if name.endswith(".wav"):
        audio = stt.load_wav("data/sample_audio/" + name)
        seconds = round(len(audio) / stt.SAMPLE_RATE, 1)
        print(name.ljust(26), str(seconds).rjust(5), "s", stt.check_audio(audio))