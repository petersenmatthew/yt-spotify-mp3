import os
import base64
from requests import post, get
import json
from dotenv import load_dotenv
import sys
import re

class SpotifyLink():
    def __init__(self, link):
        if not link:
            raise ValueError("Missing link")
        self.link = link
        
    def get_token(self):
        try:
            load_dotenv()
            client_id = os.getenv("CLIENT_ID")
            client_secret = os.getenv("CLIENT_SECRET")
            auth_string = client_id + ":" + client_secret
            auth_bytes = auth_string.encode("utf-8")
            auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

            url = "https://accounts.spotify.com/api/token"
            headers = {
                "Authorization": "Basic " + auth_base64,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {"grant_type": "client_credentials"}
            result = post(url, headers=headers, data=data)
            json_result = json.loads(result.content)
            token = json_result["access_token"]
            return token
        except KeyError:
            sys.exit("Please ensure credentials are added in the .env file. See README.md for more info")

    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token} 

    def get_spotifyid(self):
        matches = re.search(r'(track|playlist|album)/([^?]+)', self.link)
        id = matches.group(2) if matches else None

        return id

class SpotifyTrack(SpotifyLink):
    def __init__(self, link):
        super().__init__(link)
        self.id = super().get_spotifyid() 
        self.token = super().get_token()

    def track_id_to_name(self):
        try:
            url = f"https://api.spotify.com/v1/tracks/{self.id}"
            headers = super().get_auth_header(self.token)
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            name = json_result['name']
            artist = json_result['artists'][0]['name']
            return name + " - " + artist
        except KeyError:
            sys.exit("Error: Please ensure track link is valid")


class SpotifyPlaylist(SpotifyLink):
    def __init__(self, link):
        super().__init__(link)
        self.id = super().get_spotifyid() 
        self.token = super().get_token()

    def playlist_id_to_names(self):
        try:
            url = f"https://api.spotify.com/v1/playlists/{self.id}"
            headers = super().get_auth_header(self.token)
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            tracks = json_result['tracks']['items']
            track_names = []
            track_number = 0
            for track in tracks:
                track_name = json_result['tracks']['items'][track_number]['track']['name']
                track_artist = json_result['tracks']['items'][track_number]['track']['artists'][0]['name']
                track_name = track_name + " - " + track_artist
                track_names.append(track_name)
                track_number += 1
            return track_names
        except KeyError:
            sys.exit("Error: Please ensure playlist is public and existing")

    def get_playlist_name(self):
        try:
            url = f"https://api.spotify.com/v1/playlists/{self.id}"
            headers = super().get_auth_header(self.token)
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            playlist_name = json_result['name']
            playlist_owner = json_result['owner']['display_name']
            return playlist_name + " - " + playlist_owner
        except KeyError:
            sys.exit("Error: Please ensure playlist is public and existing")
        
class SpotifyAlbum(SpotifyLink):
    def __init__(self, link):
        super().__init__(link)
        self.id = super().get_spotifyid() 
        self.token = super().get_token()

    def album_id_to_names(self):
        try:
            url = f"https://api.spotify.com/v1/albums/{self.id}"
            headers = super().get_auth_header(self.token)
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            tracks = json_result['tracks']['items']
            track_names = []
            track_number = 0
            for track in tracks:
                track_name = json_result['tracks']['items'][track_number]['name']
                track_artist = json_result['tracks']['items'][track_number]['artists'][0]['name']
                track_name = track_name + " - " + track_artist
                track_names.append(track_name)
                track_number += 1
            return track_names
        except KeyError:
            sys.exit("Error: Please ensure album link is valid")
    def get_album_name(self):
        try:
            url = f"https://api.spotify.com/v1/albums/{self.id}"
            headers = super().get_auth_header(self.token)
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            album_name = json_result['name']
            album_artists = ', '.join(artist['name'] for artist in json_result['artists'])

            return f"{album_name} - {album_artists}"
        except KeyError:
            sys.exit("Error: Please ensure album link is valid")