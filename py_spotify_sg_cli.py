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
found_events = None

def get_setlist_options(answers):
    global found_setlists
    
    options = []

    for setlist in found_setlists:
        if len(setlist['sets']['set']) == 0:
            continue

        artist = setlist['artist']['name']
        date = setlist['eventDate']
        tour = setlist['tour']['name'] if 'tour' in setlist else 'No Tour Assigned'
        venue = setlist['venue']['name']
        venue_city = setlist['venue']['city']['name']

        option = "{}: {} - {}, {} - {}".format(date, artist, venue, venue_city, tour)
        options.append(option)

    options.append('Search again...')
    return options

def get_events_options(answers):
    options = []

    for event in found_events:
        try:
            option = "{}".format(event['resultsPage']['results']['event']['displayName'])
            options.append(option)
        except:
            continue

    options.append('Search again...')
    return options

setlist_query_question = [
    {
        'type': 'input',
        'name': 'setlist_query',
        'message': 'Type the name of an artist or a tour to search for setlists...'
    }
]

event_query_question = [
    {
        'type': 'input',
        'name': 'event_query',
        'message': 'Type the name of an event to search for...'
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

    # Start interacting with the user
    request_playlist_mode()

def request_playlist_mode():
    '''
    Request whether to generate from a setlist or an event
    '''
    select_mode_question = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Select a setlist you want to generate a spotify playlist for - or select \'Search again...\'',
            'choices': [
                'Create a playlist from a concerts setlist', 
                'Create a playlist from an event with multiple artists']
        }
    ]   
    answer = prompt(select_mode_question)

    if 'concerts' in answer['mode']:
        # Start the setlist mode
        start_concert_playlist_generation()
    else:
        # Start the event mode
        start_event_playlist_generation()

def start_concert_playlist_generation():
    '''
    Prompt the user to search for a concert setlist and initiate the playlist creation. 
    This is the main loop that controls interaction with the user in this mode.
    '''
    global setlist_generator
    global found_setlists
    found_setlists = {}

    answers = prompt(setlist_query_question)
    all_setlists = setlist_generator.find_concert(artist=answers['setlist_query'])

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
        start_concert_playlist_generation()
        return

    # Generate this setlist again so that we can get an index of the selected 
    # option
    setlist_options = get_setlist_options({})
    selected_option = answer['setlist_result']
    index = setlist_options.index(selected_option)
    if index != -1:
        request_concert_playlist_generation(found_setlists[index], selected_option)
    pass

def request_concert_playlist_generation(setlist, option):
    
    global setlist_generator

    print_concert_setlist(setlist)

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

    start_concert_playlist_generation()

def print_concert_setlist(setlist):
    artist = setlist['artist']['name']
    venue = setlist['venue']['name']
    venue_city = setlist['venue']['city']['name']
    tour_name = setlist['tour']['name'] if 'tour' in setlist else 'No Tour Assigned'
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

def start_event_playlist_generation():
    '''
    request the user to search for an event and initiate playlist creation.
    This ist main loop that controls interaction with the user in this mode.
    '''
    answer = prompt(event_query_question)
    search_query = answer['event_query']
    
    global found_events
    found_events = setlist_generator.find_events(search_query)

    # Print events and ask user which event to chose
    events_result_question = [
        {
            'type': 'list',
            'name': 'event_result',
            'message': 'Select an event you want to generate a spotify playlist for - or select \'Search again...\'',
            'choices': get_events_options
        }
    ]   
    answer = prompt(events_result_question)

    # Start search again if user wants to
    event_name = answer['event_result']
    if 'Search again' in event_name:
        start_event_playlist_generation()
        return

    # Find event from answer
    event = find_event_in_list(found_events, answer['event_result'])
    if not event:
        print("Error: could not get event. Please try again")
        start_event_playlist_generation()
        return

    artists = extract_event_artists(event)
    if not artists or len(artists) == 0:
        print("Error: The Songkick Website does not list any artists associated with this event.")
        print("       Please try again with a different event.")
        start_event_playlist_generation()
        return

    # List all artists so that the user can select which artists to use
    list_of_artists = [
    {
           'type': 'checkbox',
        'message': 'Select artists that will appear in your playlist. Use \'Space\' to select/deselect',
        'name': 'selected_artists',
        'choices': [],
        'validate': lambda answer: 'You must choose at least one artist.' \
            if len(answer) == 0 else True
    }
    ]

    for artist in artists:
        choice = {
            'name': artist,
            'checked' : True
        }
        list_of_artists[0]['choices'].append(choice)
    
    selected_artists = prompt(list_of_artists)['selected_artists']

    while len(selected_artists) == 0:
        print("You have to select at least one artist to generate a playlist from")
        selected_artists = prompt(list_of_artists)

    artists_confirm = [
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Do you really want to create a playlist based on the selected artists of this event?',
            'default': False
        }
    ]
    answer = prompt(artists_confirm)
    if answer['confirm']:
        url = setlist_generator.build_playlist_from_event(event_name, selected_artists)
        try:
            webbrowser.open(url)
        except:
            pass
    
    request_playlist_mode()

def extract_event_artists(event):
    '''
    From a list of songkick event jsons extract the artist names
    Songkick json scheme: https://www.songkick.com/developer/events-details
    '''
    artists = []
    try:
        for artist in event['resultsPage']['results']['event']['performance']:
            artists.append(artist['artist']['displayName'])
    except Exception as e:
        print(e)

    return artists

def find_event_in_list(events, event_name):
    for event in events:
        name = event['resultsPage']['results']['event']['displayName']
        
        if name == event_name:
            return event


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