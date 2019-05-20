from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from py_spotify_sg import SpotifySetlistGenerator
import os
import json
import sys
import webbrowser



def get_setlist_options(answers):
    options = []

    for setlist in found_setlists:
        artist = setlist['artist']['name']
        date = setlist['eventDate']
        tour = setlist['tour']['name']
        venue = setlist['venue']['name']
        venue_city = setlist['venue']['city']['name']

        option = "{}: {} - {}, {} - {}".format(date, artist, venue, venue_city, tour)
        options.append(option)

    options.append('Search again...')
    return options

setlist_query_question = [
    {
        'type': 'input',
        'name': 'setlist_query',
        'message': 'Type the name of an artist or a tour to search for setlists...'
    }
]

setlist_result_question = [
    {
        'type': 'list',
        'name': 'setlist_result',
        'message': 'Select a setlist you want to generate a spotify playlist for - or select \'Search again...\'',
        'choices': get_setlist_options
    }
]

setlist_generator = None
found_setlists = ['setlist 1', 'setlist 2']

def main():
    global setlist_generator
    
    print("Main")
    config = find_authentifications()

    setlist_generator = SpotifySetlistGenerator(config)
    request_setlistfm()

def request_setlistfm():
    '''
    Promt the user to search for a setlist and initiate the playlist creation. 
    This is the main loop that controls interaction with the user
    '''
    global setlist_generator
    global found_setlists

    answers = prompt(setlist_query_question)
    found_setlists = setlist_generator.find_setlist(artist=answers['setlist_query'])
    answer = prompt(setlist_result_question)
    
    # Start search again if user wants to
    if 'Search again' in answer['setlist_result']:
        request_setlistfm()
        return

    # Generate this setlist again so that we can get an index of the selected 
    # option
    setlist_options = get_setlist_options({})
    selected_option = answer['setlist_result']
    index = setlist_options.index(selected_option)
    if index != -1:
        request_playlist_generation(found_setlists[index], selected_option)
    pass

def request_playlist_generation(setlist, option):
    
    global setlist_generator

    setlist_confirm = [
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Do you really want to create a playlist based on the setlist of this concert:\n{}'.format(option),
            'default': False
        }
    ]

    if prompt(setlist_confirm):
        url = setlist_generator.build_setlist(setlist)

        try:
            webbrowser.open(url)
        except:
            pass
    else:
        pass

    request_setlistfm()

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
        raise e

    return {}

def request_authentifications():
    '''
    If not provided by a json file, request the access tokens from the user
    via cli
    '''
    pass

# TODO if is '__main__'
main()
