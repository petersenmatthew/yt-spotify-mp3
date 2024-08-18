import pytest
from ytsearch import get_ytid
from spotifysearch import SpotifyLink, SpotifyTrack, SpotifyAlbum, SpotifyPlaylist
from converter import findType, createlink, downloadYoutube

def test_findType():
    assert findType("New Drank - Lucki") == "title"
    assert findType("https://www.youtube.com/watch?v=RBtlPT23PTM") == "youtube_link"
    assert findType("https://open.spotify.com/track/4RVbK6cV0VqWdpCDcx3hiT?si=070ac81962e447d6") == "spotify_track"
    assert findType("https://open.spotify.com/playlist/1MSfQVdx6qmfzauozvlBYv?si=c8655ebd91474ff9") == "spotify_playlist"
    assert findType("https://open.spotify.com/album/6E3aLqi7SbbT7O78TNRtLP?si=mS2g49xYSpGz9D161F0fLA") == "spotify_album"

def test_createlink():
    assert createlink("CS50P - Lecture 8 - Object-Oriented Programming") == "https://www.youtube.com/watch?v=e4fwY9ZsxPw"

def test_downloadYoutube():
    with pytest.raises(Exception):
        downloadYoutube("youtube.com/bruh") == "1"

def test_yt_search():
    assert get_ytid("Sza - Kill Bill") == "SQnc1QibapQ"

def test_get_spotifyid():
    assert SpotifyLink("https://open.spotify.com/track/0mRbKcvmbbUtfFyfeFHCJa?si=673e7b2a16a04f1e").get_spotifyid() == "0mRbKcvmbbUtfFyfeFHCJa"

def test_track_id_to_name():
    with pytest.raises(SystemExit):
        SpotifyTrack("123").track_id_to_name()
    assert SpotifyTrack("https://open.spotify.com/track/2JzFbgbD6cc6E0YSBAAGeY?si=cdb61644414a4a84").track_id_to_name() == "Figure It Out - ian"
    assert SpotifyTrack("https://open.spotify.com/track/0SwR2Drp9MSZ11cT5QkhAQ?si=e63cc45f337f4f46").track_id_to_name() == "Highschool - FearDorian"

def test_playlist_id_to_names():
    with pytest.raises(SystemExit):
        SpotifyPlaylist("123").playlist_id_to_names()
    assert SpotifyPlaylist("https://open.spotify.com/playlist/0GhsDFjrGfxI2Apu7yxUIw?si=43c97bc02a3248e0").playlist_id_to_names()[0] == "Best Part (feat. H.E.R.) - Daniel Caesar"

def test_get_playlist_name():
    with pytest.raises(SystemExit):
        assert SpotifyPlaylist("123").get_playlist_name()
    assert SpotifyPlaylist("https://open.spotify.com/playlist/7ifKd6QBJaiRIHUrf2xWa6?si=366f902932004bb9").get_playlist_name() == "ukelele - matthrew"

def test_album_id_to_names():
    with pytest.raises(SystemExit):
        SpotifyAlbum("123").album_id_to_names()
    assert SpotifyAlbum("https://open.spotify.com/album/0lmXfHj3QJAZBpoY9jdEbV?si=bR5NC6iNT92PTA06ElyqRw").album_id_to_names()[1] == "Magic Johnson - ian"
    assert SpotifyAlbum("https://open.spotify.com/album/392p3shh2jkxUxY2VHvlH8?si=_oM0JXHATMes8Fh_qr1D7w").album_id_to_names()[9] == "Pyramids - Frank Ocean"

def test_get_album_name():
    with pytest.raises(SystemExit):
        SpotifyAlbum("123").get_album_name()

    assert SpotifyAlbum("https://open.spotify.com/album/7dAm8ShwJLFm9SaJ6Yc58O?si=WeHWFfJWSjuL8uVQxWotHw").get_album_name() == "Die Lit - Playboi Carti"
    assert SpotifyAlbum("https://open.spotify.com/album/4hvsfS6cytmO16IfAptVA9?si=D9HRsfNrTpyXgNWx1flTlA").get_album_name() == "Apollo XXI - Steve Lacy"