from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from py_spotify_sg import SpotifySetlistGenerator
import msvcrt
import os
import json
import sys
import webbrowser

def find_authentifications():
    '''
    Find a json file in the scripts directory that contains the spotify and
    setlistfm user credentials.
    '''
    try:
        script_path = os.path.normpath(__file__)
        script_dir = os.path.abspath(os.path.join(script_path, os.pardir))
        config_file = [f for f in os.listdir(script_dir) if 'config.json' in f][0]

        with open(os.path.join(script_dir, config_file), 'r') as f:
            return json.load(f)
    except Exception as e:
        pass

    return {}

config = find_authentifications()
setlist_generator = SpotifySetlistGenerator(config)
setlist_generator.find_event("Rock im Park")