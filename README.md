# py-spotify-setlist-generator
A python generator for playlists based on an artists setlist during concerts and tours.
---

Heavily inspired by this project: https://github.com/mileshenrichs/spotify-playlist-generator
And using the great work of this project: https://github.com/plamere/spotipy

---

This project is still under development and will receive some updates that make usage much easier.

---

## How to use:

### Spotify authentification:
- Log in to https://developer.spotify.com/dashboard/login and create a new app. The name of the app is up to you!
- Note the ```spotify client id``` and the ```spotify client secret```
- In the settings of your new app edit the redirect urls and add ```http://localhost/```
- In Spotify, copy the link of your spotify URI, e.g. ```spotify:user:5585525555```
- Note the part after ```user:...``` as your ```spotify user id```

[[https://github.com/username/repository/blob/master/img/octocat.png|alt=octocat]]

### Setlist.fm authentification:
- Create an setlist.fm API on https://www.setlist.fm/settings/api
- Note the ```setlist fm api key```

### Settings up the config:
- Create a ```config.json``` file in the scripts directory and add the following content. Replace the ```[...]``` with the actual values:

```
{
    "username": "[spotify user id]",
    "setlistfm-api-key" : "[setlist fm api key]",
    "spotify_client_id" : "[spotify client id]",
    "spotify_client_secret" : "[spotify client secret]"
}
```
