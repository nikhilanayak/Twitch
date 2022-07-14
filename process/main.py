import ctypes
import m3u8
import json
import os
import random
import time
from tqdm import tqdm


files = os.listdir("../data")
random.shuffle(files)


c_dll = ctypes.CDLL("/home/nikhil/Twitch/process/libmain.so")


THREADS = 128
for twitchid in tqdm(files):

    data = json.load(open(f"../data/{twitchid}/clips.json", "r"))

    if(len(data["clips"]) < 500):
        continue
    print()


    url = data["url"]["url"].replace("https", "http")


    start = time.time()


    playlist = m3u8.load(url)

    urls = [(playlist.base_uri + i.uri).encode("utf-8") for i in playlist.segments]
    files = [("/dev/shm/"+ i.uri).encode("utf-8") for i in playlist.segments]

    ctfar = ctypes.c_char_p * len(urls)


    c_urls = ctfar(*urls)
    c_files = ctfar(*files)

    c_dll.run.argtypes = [ctfar, ctfar, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    c_dll.run(c_urls, c_files, len(urls), THREADS, int(twitchid))

    end = time.time()

    print(end - start)
