from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from py_spotify_sg import SpotifySetlistGenerator
import msvcrt
import os
import json
import sys
import webbrowser

setlist_generator = None
found_setlists = ['setlist 1', 'setlist 2']

def get_setlist_options(answers):
    global found_setlists
    
    options = []

    for setlist in found_setlists:
        if len(setlist['sets']['set']) == 0:
            continue

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

def main():
    global setlist_generator
    
    print("")   
    print("Py Spotfiy Setlist Generator")
    print("============================")
    print("""
    Spotify Setlist generator is a tool that generates playlists from a concert or tour of an artist. 
    Just search for an artists name and select the setlist you want to create.
    """)
    print("For further information see: https://github.com/chr33z/py-spotify-setlist-generator")
    print("Published under MIT License - Copyright (c) 2019 Christopher Gebhardt")
    print("")
    config = find_authentifications()

    if not config:
        print("""
    Warning! No config found that contains the spotify authentification and user data.
    Please refer to print("For further information see: https://github.com/chr33z/py-spotify-setlist-generator")
    on how to create a config file.
        """)
        msvcrt.getch()
        sys.exit(0)

    print('')
    print('Connect with Spotify')
    print('====================')
    print("""
    If you start this script for the first time, a browser will open where you can connect to your
    Spotify account. When finished the browser will change to a new page. Copy the address of this
    page (URL) and enter it here.

    Press any key to continue...
        """)
    msvcrt.getch()

    setlist_generator = SpotifySetlistGenerator(config)
    request_setlistfm()

def request_setlistfm():
    '''
    Prompt the user to search for a setlist and initiate the playlist creation. 
    This is the main loop that controls interaction with the user
    '''
    global setlist_generator
    global found_setlists
    found_setlists = {}

    answers = prompt(setlist_query_question)
    all_setlists = setlist_generator.find_setlist(artist=answers['setlist_query'])

    # filter setlists where there is no setlist data
    found_setlists = [x for x in all_setlists if len(x['sets']['set']) > 0]

    setlist_result_question = [
        {
            'type': 'list',
            'name': 'setlist_result',
            'message': 'Select a setlist you want to generate a spotify playlist for - or select \'Search again...\'',
            'choices': get_setlist_options
        }
    ]   
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

    print_setlist(setlist)

    setlist_confirm = [
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Do you really want to create a playlist based on the setlist of this concert?',
            'default': False
        }
    ]
    answer = prompt(setlist_confirm)
    if answer['confirm']:
        url = setlist_generator.build_setlist(setlist)
        try:
            webbrowser.open(url)
        except:
            pass

    request_setlistfm()

def print_setlist(setlist):
    artist = setlist['artist']['name']
    venue = setlist['venue']['name']
    venue_city = setlist['venue']['city']['name']
    tour_name = setlist['tour']['name']
    date = setlist['eventDate']

    print('')
    print('Setlist:')
    print('========')
    print('{}: {} - {}, {} - {}:'.format(date, artist, venue, venue_city, tour_name))
    print('========')

    count = 1
    for song in setlist['sets']['set'][0]['song']:
        name = song['name']
        info = song['info'] if 'info' in song else ''

        # If the song name is empty then the info attribute often provides some info
        if not name and info:
            print('{}. !Info: {}'.format(count, info))
        else:
            print('{}. {}'.format(count, name))

        count += 1

    print('')

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

if __name__ == "__main__":
    main()