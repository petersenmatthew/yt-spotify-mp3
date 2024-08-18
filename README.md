# YouTube / Spotify / Song Title to MP3 - Python

A simple Python program that takes a YouTube, spotify (track or playlist), or song title and converts it to an MP3 file. 

## How To Use

Please follow the instructions listed below in order to use the converter.

### 1. Clone the repository
```
git clone https://github.com/petersenmatthew/yt-spotify-mp3.git
```
If you aren't familiar with Git, navigate to the top-left of this page and find the green button labeled "Clone or download". Clicking this and then click "Download ZIP". Extract the contents of the downloaded .zip file.

Open a terminal session and navigate to this folder, using `cd`.
```
cd yt-spotify-mp3-master/
```
### 2. Installing Dependencies

We will be installing dependencies using `pip`, the official Python package manager. 

Copy and paste (and run) the following line in your terminal session to install all necessary packages.
```
pip3 install pytube && pip3 install youtube_search && pip3 install python-dotenv
```
### 3. Setting up Spotify (Optional)

This is only required if you are planning to use this program to download spotify tracks, playlists, or albums. If not, you may ignore this.

Head to the Spotify [Dashboard](https://developer.spotify.com/dashboard/), and log in to your spotify account, Once at the Dashboard, click the green button labeled "Create App". Here, it really doesn't matter what you put for "App name" and "App description". Make sure to check both agreement boxes and click "Create".
<img width="1478" alt="Screenshot 2024-08-17 at 9 00 54 PM" src="https://github.com/user-attachments/assets/15f0442a-6318-40a4-a328-7e64131c7ca1">
<img width="1481" alt="2ndspotifyscreenshot" src="https://github.com/user-attachments/assets/05454ceb-bf3e-4ce9-a6d2-326849e806a6">



Click on your app and you should see a chart titled "Daily Active Users". Head over to the settings by clicking the button on the top right. You will see the "Client ID" field on the left. Click "View client secret" under Client ID and it should show you another long list of characters.

Copy and paste both the Client ID and the Client Secret into the .env file.

### 4. Running

You're all set, simply run in the terminal session:
```
python3 converter.py
```
All downloaded files can be found in your downloads folder.

## How It Works

This program allows the user to input a YouTube video link, Spotify link, or the title of a song to be converted into an mp3 file and stored in the user's downloads folder.

To start, the program takes the user input (a link or song title), and uses regular expressions to determine what kind of input it is through the findType() function. It then proceeds with the following based on which data type is inputted:

### 1. YouTube Link:

When a YouTube link is inputted, it is immediately passed through the downloadYoutube() function. This function uses the YouTube Object from the pytube library to access the video's audio file and download it as an mp3.

### 2. Spotify Link (Track / Playlist / Album):

When a Spotify link is inputted, it gives the input a respective class imported from the spotifysearch.py file. All of the classes are child classes of the "SpotifyLink" class, allowing it to call functions from its parent through the super() method. On initialization, it first calls the get_spotifyid() method which extracts a unique ID from the link. Then, it calls the get_token() method that loads and accesses the .env file using the dotenv and os library to return a token which is needed to use any of Spotify's API calls.

Each of these classes contains a method that returns the name and author of the track, playlist, or album. This works by using the "get" method from the requests library to make a request to the Spotify API using the id and token generated on initialization. After this, it formats the result given in JSON using the JSON library for easy access to the information received.

For playlists and albums, the request does not return a single track, but a list of tracks and their JSON data. As a result, a for loop is used to iterate over each item in the list of tracks and access the name and author of each track to be appended and returned in a new list.

After the link is converted to song titles and authors, it is then passed to the createlink() function to be further converted into a YouTube link. This function calls  get_ytid() from the ytsearch.py file which uses the youtube-search library to take a string and search for YouTube videos and return the id of the top result. The ID is then converted to a YouTube link and passed to the downloadYoutube() function mentioned above.

If the input is a playlist or album, a SpotifyAlbum or SpotifyPlaylist method is used to return the name and author of the playlist/album. The downloaded tracks are then put into a folder titled with the playlist/album name + author using the os library.

### 3. Song Title

When a song title is inputted, it is immediately passed through the createlink() function which uses get_ytid() to search YouTube with the prompt given and return the id of the most relevant result. When searching, "(Audio)" is added at the end of the search query to access audio-only videos on YouTube and avoid returning music videos that contain unnecessary audio.

The test_project.py file contains functions that test each function from all files, alongside each method from the classes in spotifysearch.py.
