import json
from pytube import Playlist, YouTube
from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError
from pyradios import RadioBrowser
from tempfile import gettempdir
import os
import mpv


st_dict = {}
st_list = []
st_json = []

def mpv_player(station):
    player = mpv.MPV(ytdl=True, input_default_bindings=True, video=False, terminal=True, input_terminal=True)
    player.play(station)
    player.wait_for_playback()

    
def mpv_player_playlist(station):
    player = mpv.MPV(ytdl=True, input_default_bindings=True, video=False, terminal=True, input_terminal=True, )
    playlist = Playlist(station)
    for i in playlist.video_urls:
        player.playlist_append(i)
    player.playlist_pos = 0
    while True:
        yt = YouTube(f"https://www.youtube.com/{player.filename}")
        player.print_text('\n' + yt.title + '\n')
        player.wait_for_playback()
        


def search_stations_by_tag(tag):
    rb = RadioBrowser()
    stations = rb.search(countrycode="ru")
    count = 0
    tmpdir = gettempdir()
    for i in stations:

        if tag in i["tags"]:
            station_name = i["name"]
            station_url = i["url"]
            station_tag = i["tags"]
            count += 1
            st_json.append(
                {
                    "key": count,
                    "name": station_name,
                    "url": station_url,
                    "tag": station_tag
                }
            )
            st_list.append(station_name)
            st_dict.update({station_name: station_url})
            # print(st_list)
    with open(f"{tmpdir}/station_{tag}.json", "w") as file:
        json.dump(st_json, file, indent=4, ensure_ascii=False)


def choice_tag():
    questions = [
        {
            'type': 'list',
            'name': 'radio_tag',
            'message': 'choice tag',
            'choices': ['russian(not all ru stations)', 'relax', 'rock', 'disco', 'pop', 'house', 'electronic', 'techno', 'chanson', 'trance', 'future', 'bass', 'news', 'jazz', 'club', 'hits', 'dance', 'hip-hop', 'rap']
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    tag = answers.get('radio_tag')
    search_stations_by_tag(tag)
    play_radio()


def play_radio():
    questions = [{
        'type': 'list',
        'name': 'Choice_Station',
        'message': 'Please choice station',
        'choices': st_list
    }]
    answers = prompt(questions, style=custom_style_2)
    station = st_dict[answers.get("Choice_Station")]
    # os.system(f'mpv --no-video {station} > /dev/null')
    mpv_player(station)

def favorites():
    f = open(os.path.expanduser("~/.config/favorites.json"), "r+")
    data = json.load(f)
    names = []
    stations = {}
    for i in data:
        name = i['name']
        url = i['url']
        names.append(name)
        stations.update({name: url})

    questions = [
        {
            'type': 'list',
            'name': 'favorites',
            'message': 'This you Favorites channel',
            'choices': names
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    station = stations[answers.get("favorites")]
    # os.system(f'mpv --no-video {station} > /dev/null')
    # mpv_player(station)
    if "playlist" in station:
        mpv_player_playlist(station)
    else:
        mpv_player(station)



def main():
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to simple radio-cli',
            'choices': ["Favorites", "Radio"]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    if answers.get("user_option") == "Favorites":
        if os.path.exists(os.path.expanduser("~/.config/favorites.json")):
            favorites()
        else:
            print('File favorites.json does not exist')
    elif answers.get("user_option") == "Radio":
        choice_tag()


if __name__ == "__main__":
    main()
