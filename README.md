# py-spotify-setlist-generator
A python generator for playlists based on an artists setlist during concerts and tours.
---

Heavily inspired by this project: https://github.com/mileshenrichs/spotify-playlist-generator
And using the great work of this project: https://github.com/plamere/spotipy

![Spotify Setlist Generator Usage](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/usage.gif)

## How to use:
For the first use there are some steps you have to do in order to use the tool. These steps have to be performed once(!) for a user. When you are comfortable with sharing your spotify ```client id``` and ```client secret``` (see below) you only have to change the ```spotify user id``` to share the tool.

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
- Note the part after ```user:...``` as your ```spotify user id```
![Spotify User ID](https://github.com/chr33z/py-spotify-setlist-generator/blob/master/img/spotify_user_id.png)

### Setlist.fm authentification:
- Create an setlist.fm API on https://www.setlist.fm/settings/api
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

### First time authentification with Spotify
Upon the first start of the tool you have to confirm access of this tool to your spotify account. For this a browser windows is opened where you can enter your credentials. **Your will be redirected to page ```http://localhost/?code=...```. Copy the URL and paste it in the tools terminal window.**
