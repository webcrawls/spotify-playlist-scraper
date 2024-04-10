import json
import os
import pathlib
import sys

import requests


def main():
    if not os.path.exists('playlists'):
        print("no playlists/ directory found! run main.py first!")
        print("exiting...")
        sys.exit(1)
        return

    pathlib.Path('images/').mkdir(exist_ok=True, parents=True)

    images = {}

    for file in os.listdir('playlists'):
        if not file.endswith('.json'):
            continue

        with open('playlists/' + file, 'r') as f:
            playlist = json.load(f)
            if not 'image_url' in playlist:
                continue
            url = playlist['image_url']
            images[file] = url

    for [name, url] in images.items():
        r = requests.get(
            url,
            stream=True)
        ext = r.headers['content-type'].split('/')[
            -1]  # converts response headers mime type to an extension (may not work with everything)

        with open("./images/%s.%s" % (name, ext), 'wb') as g:  # open the file to write as binary - replace 'wb' with 'w' for text files
            for chunk in r.iter_content(1024):  # iterate on stream using 1KB packets
                g.write(chunk)  # write the file
                g.flush()


main()
