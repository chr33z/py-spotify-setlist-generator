import requests
import urllib.parse
import spotipy
import spotipy.util as sputil
import pprint

class SpotifySetlistGenerator():

    spotify_auth = ''
    setlistfm_auth = ""

    def __init__(self, config):
        '''
        Initialize the generator by providing spotify and setlistfm authentification
        credentials.

        :param str spotify_auth: spotify authentification
        :param str setlistfm_auth: setlistfm authentification
        '''
        self.config = config

        client_id = config['spotify_client_id']
        client_secret = config['spotify_client_secret']
        username = config['username']
        scope = 'playlist-modify-public'
        self.token = sputil.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost/')

    def find_setlist(self, artist, tour='', limit=10):
        '''
        Find a setlist on setlist.fm by searching for an artist, venue or tour
        :param str artist: A string containing the artists name
        :param str tour: A string containing the tour name (optional)
        :return setlists: list of found setlists (see for further info: https://api.setlist.fm/docs/1.0/ui/index.html#//1.0/search/setlists)
        '''
        artist = urllib.parse.quote(artist)
        tour = urllib.parse.quote(tour)

        query_params = ''
        if tour:
            query_params = '/setlists?artistName={}&p=1&tourName={}'.format(artist, tour)
        else:
            query_params = '/setlists?artistName={}&p=1'.format(artist)

        headers = self.setlistfm_auth_header(self.config)
        r = requests.get('https://api.setlist.fm/rest/1.0/search' + query_params, headers=headers)
        res = r.json()

        if r.status_code == 404:
            return {}
        else:
            # Returns a list of setlist dictionaries
            # Json model can be found here: https://api.setlist.fm/docs/1.0/ui/index.html#//1.0/search/setlists
            return res['setlist']

    def build_setlist(self, setlist):
        '''
        From a given setlist, find the songs on spotify and create a playlist with
        the title of the tour and the artist

        :param str setlist: list of songs of an artist as dictionary
        '''
        artist = setlist['artist']['name']
        tour_name = setlist['tour']['name']
        date = setlist['eventDate']
        playlist_name = '{} - {} - {}'.format(artist, tour_name, date[-4:])

        songs_not_found = []
        song_ids = []
        for song in setlist['sets']['set'][0]['song']:
            id = self.find_song_on_spotify(artist, song['name'])
            if id:
                song_ids.append(id)
            else:
                songs_not_found.append(song['name'])

        playlist_url = self.create_playlist(playlist_name, song_ids)

        # TODO raise some exception if playlist could not be created
        return playlist_url

    def find_song_on_spotify(self, artist, song):
        '''
        Query the spotify api to search for a song id of a given song of an artist

        :param str artist: Name of the artist
        :param str song: Name of the song
        :return song_id: spotify id of the song
        '''
        sp = spotipy.Spotify(self.token)
        result = sp.search('{} {}'.format(artist, song))
        try:
            return result['tracks']['items'][0]['id']
        except:
            return ''

    def create_playlist(self, playlist_name, song_ids):
        '''
        Create a playlist with a given name and add all provides song ids.
        The playlist will be added to the spotify users account

        :param str playlist_name: Name of the playlist
        :param str list of spotify song ids
        '''

        description = '''
        'This playlist was built by a script.  Heavily inspired by this project: https://github.com/mileshenrichs/spotify-playlist-generator'
        '''
        sp = spotipy.Spotify(self.token)
        sp.trace = True
        playlist = sp.user_playlist_create(self.config['username'], playlist_name, public=True)
        results = sp.user_playlist_add_tracks(self.config['username'], playlist['id'], song_ids)

        return playlist['external_urls']['spotify']

    def add_songs_to_playlist(self, playlist_id, song_ids):
        '''
        Add songs to an existing playlist on spotify

        :param str playlist_id: spotify id of the playlist
        :param str song_ids: list of spotify song ids
        '''
        # get user id (used in request)
        c.execute("SELECT value FROM tokens WHERE token_type = 'spotify_id'")
        userId = c.fetchone()[0]

        # send request to add tracks to Spotify playlist
        reqHeader = {'Authorization': 'Bearer {}'.format(spotifyToken), 'Content-Type': 'application/json'}
        reqBody = {'uris': list(map((lambda song_id: 'spotify:track:' + song_id), song_ids))}

        post_url = 'https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(userId, playlist_id)
        r = requests.post(post_url, headers=reqHeader, json=reqBody)

    def setlistfm_auth_header(self, config):
        return {
            'x-api-key' : config['setlistfm-api-key'],
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
        }