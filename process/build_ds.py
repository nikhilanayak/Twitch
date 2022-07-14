import json
import matplotlib.pyplot as plt
import os
import random



files = iter(os.listdir("dumps"))
#id = random.choice(files)


def run(id):
    print(f"file: {id}")
    data = json.load(open(f"../data/{id.split('.')[0]}/clips.json"))


    clips = data["clips"]


    if len(clips) < 500:
        #print(len(clips))
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
    #print(secs)

    print(max(set(secs), key=secs.count))

    return True


while not run(next(files)):
    pass
