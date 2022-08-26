import requests
import json
from pprint import pprint
import webbrowser

# Get a token here: https://developer.spotify.com/console/post-playlists/?user_id=&body=%7B%22name%22%3A%22New%20Playlist%22%2C%22description%22%3A%22New%20playlist%20description%22%2C%22public%22%3Afalse%7D
my_token = "enter your token here"
auth_token = {"Authorization" : f"Bearer {my_token}"}

# Searching for artist
artist = input("Enter any artist: ").title()
header2 = {"q" : f"artist:{artist}","type" : "artist","market" : "US", "limit" : "5"}
response = requests.get(" https://api.spotify.com/v1/search", headers = auth_token, params = header2)
# print(response)
artist_search = response.json()

# pprint(artist_search)
# print(artist_search['artists']['items'][0]['name'])
num = 1
artist_id = str()
for result in artist_search['artists']['items']:
    print (str(num) + ") " + result['name'])
    num = num + 1
pick = int(input("Which result matches the artist you were searching for? "))

if(pick == 1):
    artist_id = artist_search['artists']['items'][0]['id']
elif(pick == 2):
    artist_id = artist_search['artists']['items'][1]['id']
elif(pick == 3):
    artist_id = artist_search['artists']['items'][2]['id']
elif(pick == 4):
    artist_id = artist_search['artists']['items'][3]['id']
else:
    artist_id = artist_search['artists']['items'][0]['id']

num = 1
# print(artist_id)

# # Creating list of top tracks
artist_top_tracks = []
uris_for_tracks = []

response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US", headers = auth_token)
# print(response)
json_response = response.json();
# print(json_response)
for track in json_response['tracks']:
    artist_top_tracks.append(track['name'])
    uris_for_tracks.append(track['uri'])
    # print(track['name'])
# print(str(uris_for_tracks))
print(f"{artist}'s top tracks")
for track in artist_top_tracks:
    print(f"{num}) {track}")
    num += 1

response = requests.get("https://api.spotify.com/v1/me", headers = auth_token)
get_id_response = response.json();
# print(get_id_response)
user_id = get_id_response['id']
# print(user_id)

data = {"name": f"{artist}'s Top Tracks","description": f"A playlist of {artist}'s top tracks made by me on PYTHON!"}
json_data = json.dumps(data)
response = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", headers = auth_token, data = json_data)
# print(response)
string_of_tracks = str()
playlist_id = response.json()['id']
for track_id in uris_for_tracks:
    if uris_for_tracks.index(track_id) == len(uris_for_tracks) - 1:
        string_of_tracks += (track_id)
    else:
        string_of_tracks += (track_id + ",")
header3 = {"uris" : string_of_tracks}
response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",headers = auth_token, params = header3)
# print(response.json())

print(f"A playlist of {artist}'s top 10 songs has been added to your spotify! Go check it out.")
webbrowser. open(f'https://open.spotify.com/playlist/{playlist_id}')
# Adding Top Tracks to playlists
