import m3u8
import librosa
import tempfile
import urllib.request
import numpy as np
import scipy.io.wavfile



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
    



if __name__ == "__main__":
    url = "https://d2vjef5jvl6bfs.cloudfront.net/6193974c123fd307b218_marzzzzy_46737524461_1656968794/audio_only/index-dvr.m3u8"
    #build(url, None)
    gen = M3Q(url)

    xs = []
    for i in range(1):
        xs += next(gen)
        
    scipy.io.wavfile.write(f"out.wav", 44100, np.array(xs))
        

    #for ind, i in enumerate(gen):
    #    scipy.io.wavfile.write(f"{ind}.wav", 44100, np.array(i))
        #print(ind)




