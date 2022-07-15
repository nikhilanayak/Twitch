import ctypes
import m3u8
import json
import os
import random
import time
from tqdm import tqdm

os.environ["TMP"] = "/dev/shm/"


files = os.listdir("../data")
random.shuffle(files)


c_dll = ctypes.CDLL("/home/nikhil/Twitch/process/libmain.so")


for twitchid in tqdm(files):

    data = json.load(open(f"../data/{twitchid}/clips.json", "r"))

    if(len(data["clips"]) < 500):
        continue
    print()


    url = data["url"]["url"].replace("https", "http")

    os.system(f"python3 -m twitchdl download {twitchid} -q audio_only -w 128 -o dumps/{twitchid}.mkv")
