# Py Spotify Setlist Generator
A python generator for playlists based on an artists setlist during concerts.
---

## Why:
Do you have one of these friends? For every concert and festival they visit they create these carefully curated playlists on spotify containing every track the band will play on this particular evening - just to put them on social media to share with their friends. Now you can do that too, even without carefully curating anything! 

![Spotify Setlist Generator Usage](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/usage.gif)

## How to use:
When using this tool for the first time there are some steps you have to do. These steps have to be only performed once(!) for a user. When you are comfortable with sharing your spotify ```client id``` and ```client secret``` (see below) you only have to change the ```spotify user id``` to share the tool.

This tool uses a ```config.json``` file to provide the authentification and api keys. Read on to see how to create your own config.json. 

### Requirements
- Try the windows binaries in [coming soon]
- Else: 
  - Python 3.7
  - Some modules

### Spotify authentification:
- Log in to https://developer.spotify.com/dashboard/login and create a new app. The name of the app is up to you!
- Note the ```spotify client id``` and the ```spotify client secret```

![Spotify Dashboard](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/spotify_dashboard.png)

- In the settings of your new app edit the redirect urls and add ```http://localhost/```

![Spotify Edit Settings](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/spotify_edit_settings.png)

- In Spotify, copy the link of your spotify URI, e.g. ```spotify:user:5585525555```
- Note the part after ```user:...``` as your ```spotify user id```, so e.g. ```5585525555```

![Spotify User ID](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/spotify_user_id.png)

### Setlist.fm authentification:
- Create an setlist.fm API key on https://www.setlist.fm/settings/api
- Note the ```setlist fm api key```

### Setting up the config:
- Create a ```config.json``` file in the scripts directory and add the following content. Replace the ```[...]``` with the actual values:

```
{
    "username": "[spotify user id]",
    "setlistfm-api-key" : "[setlist fm api key]",
    "spotify_client_id" : "[spotify client id]",
    "spotify_client_secret" : "[spotify client secret]"
}
```

### First time startup and authentification with Spotify
The tool is started by running ```py_spotify_sg_cli.py```, you may have to install some dependencies [info on that tbc]

When the tool is started for the first time you have to grant access to your spotify account. To do this, a browser windows is opened where you can enter your credentials. **When the operation was successfull you will be redirected to another page ```http://localhost/?code=...```. Copy the whole URL and paste it in the tools terminal window. See the instructions of the tool for more information.**

## Further Development
- [ ] Search for festivals and create playlists based on the bands playing there
- [ ] Create a gui version

## Acknowledgements
Heavily inspired by this project:
- https://github.com/mileshenrichs/spotify-playlist-generator

And using the great work of these projects:
- https://github.com/plamere/spotipy
- https://github.com/CITGuru/PyInquirer
