import os
import matplotlib.pyplot as plt
import json
import librosa
import numpy as np


procced = list(map(lambda x: x.replace(".ts", ""), os.listdir("../process/dumps")))
os.chdir("..")


id = procced[0]

data = json.load(open(f"data/{id}/clips.json"))

clips = data["clips"]

secs = []

for i in clips:
    i = i["node"]

    duration = i["durationSeconds"]
    voffset = i["videoOffsetSeconds"]

    for x in range(voffset, voffset + duration):
        secs.append(x)



