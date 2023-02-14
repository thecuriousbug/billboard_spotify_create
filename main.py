from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#--------------------------------- part -1 ---------------------------------------------#
date = input("enter the date in YYYY-MM-DD fromat")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text , "html.parser")
raw_data = soup.find_all(name="h3" , id="title-of-a-story" , class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")


songs = [song.getText() for song in raw_data]


clean_data = [data.strip().replace('\n', '').replace('\t', '') for data in songs]
#print(clean_data)


#------------------------------------------part -2----------------------------------------------------#
clinet_id = "f9b40b56c1da413e942b183c2578ae34"
client_secret = "95d4c82e6aa54f6986c258ee0c9478d0"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="f9b40b56c1da413e942b183c2578ae34",
        client_secret="95d4c82e6aa54f6986c258ee0c9478d0",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

#-----------------------------------part -3 -----------------------------------------------------------#
song_uris = []
year = date.split("-")[0]
for song in clean_data:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#print(song_uris)

#----------------------------------- part -4 --------------------------------------------------------#
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)