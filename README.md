# spotify-playlist-scraper

A handful of Python scripts that can be used to scrape a personal Spotify account's playlist information.

## Installation

This repo should work on any platform.

Ensure Python `3.11` is installed (presumably later versions will work), and `git clone` this repository somewhere on
your computer.

Run the following commands in the root directory:

- `python -m venv env`
-
    - On *nix: `source env/bin/activate`
    - On Windows: `source env/Scripts/activate`
- `pip install -r requirements.txt`

## Usage

Ensure you have `source`'d the Python environment, and run `main.py`:

```
python main.py

# Only download playlists matching a glob/string:
python main.py --only Favs
python main.py --only *'s Playlist
```

The script will authenticate a Spotify application ([which you should create](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) and provide the credentials in a `.env`
file, see `.env.EXAMPLE`), which will iterate over your playlists and save them to `.json` files in the `playlists/`
folder.

Currently, the script saves:
- the name of the track/episode
- the artist
- the spotify URL
- the custom playlist image URL, if any