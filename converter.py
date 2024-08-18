from pytube import YouTube
import re
from ytsearch import get_ytid
from spotifysearch import SpotifyLink, SpotifyTrack, SpotifyAlbum, SpotifyPlaylist
import os 

# MUST NEEDED LIBRARIES ⬇️

# pip install pytube
# pip install youtube_search
# pip install python-dotenv


def main():
    user_input = input("Link / Title: ")
    input_type = findType(user_input)
    
    try:
        if input_type == "youtube_link":
            downloadYoutube(user_input)
        elif input_type == "spotify_track":
            track_name = SpotifyTrack(user_input).track_id_to_name()
            downloadYoutube(createlink(track_name))
        elif input_type == "spotify_playlist":
            playlist_id = SpotifyLink(user_input).get_spotifyid()
            songs_in_playlist = SpotifyPlaylist(user_input).playlist_id_to_names()
            for song in songs_in_playlist:
                downloadYoutube(createlink(song), is_playlist=True, playlist_id=playlist_id)
            print("Playlist has finished downloading")
        elif input_type == "spotify_album":
            album_id = SpotifyLink(user_input).get_spotifyid()
            songs_in_album = SpotifyAlbum(user_input).album_id_to_names()
            for song in songs_in_album:
                downloadYoutube(createlink(song), is_album=True, album_id=album_id)
            print("Album has finished downloading")
        elif input_type == "title":
            downloadYoutube(createlink(user_input))
        else:
            print("Invalid link. Please enter a Spotify link, Youtube link, or the title of a song.")
    except NameError:
        print("Error: Please add spotify credentials to .env file - see README.md")
        
def findType(n):
    matches_link = re.search(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", n)
    if matches_link:
        matches_youtube = re.search(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", n)
        matches_spotify_track = re.search(r"(https?:\/\/open.spotify.com\/track\/[a-zA-Z0-9]+|spotify:track:[a-zA-Z0-9]+)", n)
        matches_spotify_playlist = re.search(r"(https?:\/\/open.spotify.com\/playlist\/[a-zA-Z0-9]+|spotify:playlist:[a-zA-Z0-9]+)", n)
        matches_spotify_album = re.search(r"(https?:\/\/open.spotify.com\/album\/[a-zA-Z0-9]+|spotify:album:[a-zA-Z0-9]+)", n)
        if matches_youtube:
            return "youtube_link"
        elif matches_spotify_track:
            return "spotify_track"
        elif matches_spotify_playlist:
            return "spotify_playlist"
        elif matches_spotify_album:
            return "spotify_album"
        else:
            raise ValueError("Invalid Link")
    else:
        return "title"
    
def createlink(title):
    id = get_ytid(title)
    link = "https://www.youtube.com/watch?v=" + id
    return link

def downloadYoutube(link, is_playlist=False, is_album=False, playlist_id=None, album_id=None):
        try:

            if os.name == "nt":
                DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
            else:
                DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads"

            if is_playlist:
                playlist_name = SpotifyPlaylist(f"https://open.spotify.com/playlist/{playlist_id}?").get_playlist_name()
                playlist_folder = os.path.join(DOWNLOAD_FOLDER, playlist_name)
                os.makedirs(playlist_folder, exist_ok=True)
                output_path = playlist_folder
            elif is_album:
                album_name = SpotifyAlbum(f"https://open.spotify.com/playlist/{album_id}?").get_album_name()
                album_folder = os.path.join(DOWNLOAD_FOLDER, album_name)
                os.makedirs(album_folder, exist_ok=True)
                output_path = album_folder
            else:
                output_path = DOWNLOAD_FOLDER

            video = YouTube(link)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(output_path=output_path, filename=f"{video.title}.mp3")
            print(f"{video.title} has been downloaded in MP3")
        except KeyError:
            print("Unable to fetch video information. Please check the video URL or your network connection.")



if __name__ == "__main__":
    main()