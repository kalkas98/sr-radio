import json
import requests

SR_CHANNELS_URL = "https://api.sr.se/api/v2/channels?pagination=false&format=json"
SR_PLAYLIST_URL = "https://api.sr.se/api/v2/playlists/rightnow?channelid="
RADIO_STATION_FILE = "resources/radio_stations.txt"

class Station:
   def __init__(self, name, id, url):
       self.name = name
       self.id = id
       self.url = url
       self.currentSongDesc = ""
       self.currentSongEndDate = ""


def get_current_song_info(channel_id):
    json_data = get_json_data(SR_PLAYLIST_URL+str(channel_id)+"&format=json")
    print("channel id",channel_id)
    if "song" in json_data["playlist"]:
        song = json_data["playlist"]["song"]
        return (song["title"], song["artist"], song["stoptimeutc"])

def get_json_data(url):
    """Makes a HTTP request with the given url and returns json data as a python object"""
    raw_json = requests.get(url)
    try:
        json_data = json.loads(raw_json.content)
    except json.JSONDecodeError:
        print("Error: Got non valid JSON document from", url)
        raise
    return json_data

def get_sr_channel_dict():
    """Returns a dictionary containing the channel names as keys and their URL:s as value"""
    channel_dict = {}
    json_data = get_json_data(SR_CHANNELS_URL)
    for channel in json_data["channels"]:
        new_channel = Station(channel["name"], channel["id"], channel["liveaudio"]["url"])
        channel_dict[channel["name"]] = new_channel
    return channel_dict
    