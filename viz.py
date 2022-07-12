import os
import random
import json
import matplotlib.pyplot as plt
from tqdm import tqdm


class Average:
    def __init__(self):
        self.sum = 0
        self.ct = 0
        pass

    def add(self, o):
        self.sum += o
        self.ct += 1


    def eval(self):
        return self.sum / self.ct


files = os.listdir("data")


avgClips = Average()
avgLen = Average()

i = 0

secs = 0

for f in tqdm(files):
    data = json.load(open(f"data/{f}/clips.json", "r"))
    clips = data["clips"]


    if len(clips) < 500:
        continue

    i += 1


    avgClips.add(len(clips))
    avgLen.add(data["len"])

    secs += data["len"]
    

print(f"average clips: {avgClips.eval()}")
print(f"average video length: {avgLen.eval()} seconds")
print(f"full secs: {secs}")
print(f"num points: {i}")

quit()




def run(id):

    data = json.load(open(f"data/{id}/clips.json", "r"))

    clips = data["clips"]


    if len(clips) < 500:
        print(len(clips))
        return False

    print(f"{data['len']} seconds")
    print(f"{len(clips)} clips")

    #secs = [0 for i in range(data["len"])]
    secs = []

    for i in clips:
        i = i["node"]

        duration = i["durationSeconds"]
        voffset = i["videoOffsetSeconds"]

        for x in range(voffset, voffset + duration):
            #for j in range(i["viewCount"]):
            secs.append(x)


    plt.hist(secs, bins=100)
    plt.show()

    return True



id = random.choice(os.listdir("data"))
while not run(id):
    id = random.choice(os.listdir("data"))
    pass
