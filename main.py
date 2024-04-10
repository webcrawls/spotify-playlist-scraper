import argparse
import datetime
import fnmatch
import json
import os
import pathlib

import spotipy
import spotipy.util as util
import termcolor
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description='Read Spotify playlist data into .jsons.')
parser.add_argument('-o', '--only')
args = vars(parser.parse_args())

def setup_spotify() -> spotipy.Spotify:
    """ Generate the token. Please respect these crdentials :) """
    credentials = spotipy.SpotifyOAuth(scope="playlist-read-private,playlist-read-collaborative")
    spotify = spotipy.Spotify(auth_manager=credentials)
    return spotify

def write_playlist(spotify: spotipy.Spotify,
                   playlist: object):
    print(termcolor.colored("Loading playlist ", 'cyan') + termcolor.colored(playlist['name'], 'light_cyan'))
    results = spotify.playlist_items(playlist['id'])

    output_object = {}

    if 'images' in playlist['object']:
        image = playlist['object']['images'][0]
        output_object['image_url'] = image['url']

    tracks_result = results['items']
    new_tracks = get_tracks(tracks_result)
    page = 0

    results_temp = results
    while results_temp['next']:
        print("Paging playlist "+playlist['name'] +"("+str(page)+")")
        results_temp = spotify.next(results_temp)
        new_tracks.extend(get_tracks(results_temp['items']))
        page += 1

    output_object['tracks'] = new_tracks

    print("Found "+str(len(output_object['tracks'])) +" songs")

    filename = 'playlists/'+playlist['name'].replace(' ', '_')+".json"
    pathlib.Path('playlists').mkdir(parents=True, exist_ok=True)

    with open(filename, 'w+') as file:
        json.dump(output_object, file)
        print(termcolor.colored("Written to ", 'cyan') + termcolor.colored(filename, 'light_cyan'))

def get_tracks(tracks):
    track_output = []

    for track in tracks:
        # print(track.keys())
        track_object = {}

        try:
            if 'description' in track['track']:
                track_object['description'] = track['track']['description']

            if 'href' in track['track']:
                track_object["spotify_href"] = track['track']['href']

            if track['track']['type'] == 'episode':
                # sometimes you got a joe rogan in the playlist fuck it gotta be honest
                track_object["name"] = track['track']['name']
                track_object["artist"] = track['track']['artists'][0]['name']
            else:
                track_object["name"] = track['track']['name']
                track_object["artist"] = track['track']['artists'][0]['name']
        except Exception as e:
            print("error!", track_object, track)
            print(e)

        track_output.append(track_object)

    return track_output

def get_playlists(spotify: spotipy.Spotify):
    playlists = spotify.current_user_playlists()

    playlists_formatted = []

    for playlist in playlists['items']:
        name = playlist['name']

        if args['only']:
            # handle --only flag logic
            matches = fnmatch.filter([name], args['only'])
            if len(matches) == 0:
                continue

        playlists_formatted.append({ "name": name, "id": playlist['id'], "object": playlist })

    for playlist in playlists_formatted:
        write_playlist(spotify, playlist)


print("spotify-playlist-scraper", datetime.datetime.now())
print("")
print("Hello! I will scrape your Spotify playlists.")
print("")
print(termcolor.colored("Before we begin, be aware that I will open a page", 'red'))
print(termcolor.colored("in your browser, which will request to grant me", 'red'))
print(termcolor.colored("the permission to read your private and collaborative playlists.", 'red'))
print("")
print(termcolor.colored("After you grant authorization, you will be redirected to a blank page", 'light_green'))
print(termcolor.colored("with a URL starting with", 'light_green'), termcolor.colored('"localhost/"', 'light_cyan')+ termcolor.colored('. Copy this URL', 'light_green'))
print(termcolor.colored('into this script to start the scraping process.', 'light_green'))
print("")
print(termcolor.colored("You may revoke these permissions when the script finishes by", 'yellow'))
print(termcolor.colored("visiting", 'yellow'), termcolor.colored("https://www.spotify.com/us/account/apps/", 'cyan'))
print(termcolor.colored('and removing', 'yellow'), termcolor.colored('spotify-playlist-scraper', 'cyan') + termcolor.colored("'s access.", 'yellow'))
print("")

input("Press ENTER to begin >")
spotify = setup_spotify()
get_playlists(spotify)