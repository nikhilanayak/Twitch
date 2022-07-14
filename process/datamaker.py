import m3u8
import librosa
import tempfile
import urllib.request
import numpy as np
import scipy.io.wavfile
from multiprocessing import Pool
from threading import Lock

done = 0
dLock = Lock()

def save(url):
    global done

    raw_ts = urllib.request.urlopen(url)
    
    fname = url.rsplit("/", 1)[1]

    with open(f"/dev/shm/{fname}", "wb") as of:
        of.write(raw_ts.read())

    
    with dLock:
        #done -= 1
        print("done")
    #print("finished")
    #return f"/dev/shm/{fname}"



def M3Thread(url):
    global done

    playlist = m3u8.load(url)

    segments = [playlist.base_uri + i.uri for i in playlist.segments]

    done = len(segments)
    print(done, "segments")

    
    with Pool(256) as p:
        res = p.map(save, segments)





"""
def save(base_url, url):
    raw_ts = urllib.request.urlopen(base_url + url)
    with open(f"/dev/shm/{url}", "wb") as of:
        of.write(raw_ts.read())
    return f"/dev/shm/{url}"


def M3Q(base_url, bs_seconds=1):
    playlist = m3u8.load(base_url)

    urls = [seg.uri for seg in playlist.segments]
    running_data = []

    while True:
        if len(running_data) > 44100:
            out = running_data[:44100]
            running_data = running_data[44100:]

            yield out

        else:
            if len(urls) > 0:
                curr, sr = librosa.load(save(playlist.base_uri, urls.pop()))
                curr = list(curr)

                running_data += curr
            else:
                return

"""    


if __name__ == "__main__":
    url = "https://dqrpb9wgowsf5.cloudfront.net/ffaae97ace5de4ec9653_apply_40953784907_1657169034/audio_only/index-dvr.m3u8"

    M3Thread(url)
    
