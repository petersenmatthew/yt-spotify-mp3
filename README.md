# YouTube / Spotify / Song Title to MP3 - Python

A simple program that takes a YouTube, spotify (track or playlist), or song title and converts it to an MP3 file in python. 

## How To Use

Please follow the instructions listed below in order to use the converter.

1. Clone the repository

git clone https://github.com/petersenmatthew/spotify-to-mp3-python.git

If you aren't familiar with Git, navigate to the top-left of this page and find the green button labeled "Clone or download". Clicking this and then click "Download ZIP". Extract the contents of the downloaded .zip file.

Open a terminal session and navigate to this folder, using cd.

cd spotify-to-mp3-python/

2. Installing Dependencies

We will be installing dependencies using pip, the official Python package manager. If you do not have pip, I'd recommend checking this thread to install it.

Copy and paste (and run) the following line in your terminal session to install all necessary packages.

pip3 install pytube && pip3 install youtube_search && pip3 install python-dotenv

3. Setting up Spotify (Optional)

This is only required if you are planning to use this program to download spotify tracks, playlists, or albums. If not, you may ignore this.

Head to the Spotify Dashboard, and log in to your spotify account, Once at the Dashboard, click the green button labeled "Create App". Here, it really doesn't matter what you put for "App name" and "App description". Make sure to check both agreement boxes and click "Create".

You will see the "Client ID" field on the left (it's redacted here). Click "Show client secret" under Client ID and it should show you another long list of characters.

Copy and paste both the Client ID and the Client Secret into the .env file.

4. Running

You're all set, simply run in the terminal session:

python3 main.py

All downloaded files can be found in your downloads folder.


## Description

This program allows the user to input a YouTube video link, Spotify link, or the title of a song to be converted into an mp3 file and stored in the user's DOWNLOADS folder.

To start, the program takes the user input (a link or song title), and uses regular expressions to determine what kind of input it is through the findType() function. It then proceeds with the following based on which data type is inputted:

1. YouTube Link:

When a YouTube link is inputted, it is immediately passed through the downloadYoutube() function. This function uses the YouTube Object from the pytube library to access the video's audio file and download it as an mp3.

2. Spotify Link (Track / Playlist / Album):

When a spotify link is inputted, it gives the input the a respective class which is imported from the spotifysearch.py file. All of the classes are child classes of the "SpotifyLink" class, allowing it to call functions from its parent through the super() method. On initalization, it firstly calls the get_spotifyid() method which extracts a unique id from the link. Then, it calls then get_token() method that loads and acceses the .env file using the dotenv and os library to return a token which is needed to use any of Spotify's API calls. 

Each of these classes contains a method that returns the name and author of the track, playlist, or album. This works by using the "get" method from the requests library to make a request to the Spotify API using the id and token generated on initialization. After this, it formats the result given in JSON using the json library for easy access to the information received. 

For playlists and albums, the request does not return a single track, but a list of tracks and their JSON data. As a result, a for loop is used to iterate over each item in the list of tracks and access the name and author of each track to be appended and returned in a new list. 

After the link is converted to song titles and authors, it is then passed to the createlink() function to be further converted into a YouTube link. This function calls  get_ytid() from the ytsearch.py file which uses the youtube-search library in order to take a string and search for YouTube videos and return the id of the top result. The id is then converted to a YouTube link and passed to the downloadYoutube() function mentioned above. 

If the input is a playlist or album, a SpotifyAlbum or SpotifyPlaylist method is used to return the name and author of the playlist / album. The downloaded tracks are then put into a folder titled with the playlist / album name + author using the os library. 

3. Song Title

When a song title is inputted, it is immediately passed through the createlink() function which uses get_ytid() to search YouTube with the prompt given and return the id of the most relevant result. When searching, "(Audio)" is added at the end of the search query in order to access audio-only videos on YouTube and avoid returning music videos that contain unnessecary audio.

The test_project.py file contains functions that test each function from all files, alongside each method from the classes in spotifysearch.py.
