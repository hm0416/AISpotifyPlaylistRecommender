import requests
import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

#Having this gives us a single point of control over most 0.0 to 1.0 intervals
def norm_selection(num):
    #0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    #Filter method for selection
    if num < 0.33:
        return 'l'
    elif num < 0.66:
        return 'm'
    else:
        return 'h'

def tempo_selection(tempo):
    if tempo <= 60:
        #largo
        return 'l'
    elif tempo <= 66:
        #larghetto
        return 'o'
    elif tempo <= 76:
        #adagio
        return 'a'
    elif tempo <= 108:
        #adante
        return 'e'
    elif tempo <= 120:
        #moderato
        return 'm'
    elif tempo <= 168:
        #allegro
        return 'r'
    elif tempo <= 200:
        #presto
        return 'p'
    elif tempo > 200:
        #prestissimo
        return 'i'

def loudness_selection(score):
    if score <= -40:
        return 'l'
    elif score <= -20:
        return 'm'
    elif score <= 0:
        return 'h'

#Converts continous variables to descrete and writes the line
#I'm so sorry but there is no better way to do this since each feature has a different numerical range.. Thanks spotify
#Output: dec danceability energy loudness speechiness acousticness instrumentalness liveness valence tempo
def line_feature_selector(song, dec, outFile):
    features = spotify.audio_features(song)[0]
    #danceability -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    danceability = norm_selection(features['danceability'])
    #energy -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    energy = norm_selection(features['energy'])
    #loudness -- -60db to 0db
    loudness = loudness_selection(features['loudness'])
    #speechiness -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    speechiness = norm_selection(features['speechiness'])
    #acousticness -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    acousticness = norm_selection(features['acousticness'])
    #instrumentalness -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    instrumentalness = norm_selection(features['instrumentalness'])
    #liveness -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    liveness = norm_selection(features['liveness'])
    #valence -- 0.0 to 1.0 | l --> (0.0 upto 0.33), m --> (0.33 upto 0.66), h --> (0.66 to 1.00)
    valence = norm_selection(features['valence'])
    #tempo -- prestissimo (>200 bpm), presto (168–200 bpm), allegro (120–168 bpm), moderato (108–120 bpm), andante (76–108 bpm), adagio (66–76 bpm), larghetto (60–66 bpm), and largo (40–60 bpm)
    tempo = tempo_selection(features['tempo'])
    outStr = dec + "," + danceability + "," + energy + "," + loudness + "," + speechiness + "," + acousticness + "," + instrumentalness + "," + liveness + "," + valence + "," + tempo + "\n"
    outFile.write(outStr)
    

def outputCSVTrain(userSet):
    #Opens file and either overwrites it or creates a new file
    if os.path.exists("train.csv"):
        #Overwrites
        toFile = open("train.csv", "w")
    else:
        #Creates new
        toFile = open("train.csv", "x")

    for song in userSet:
        #NOTE: song is URI now in this context, the key for "userSet"
        line_feature_selector(song, userSet[song], toFile)

    toFile.close()


def outputCSVTest(userSet):
    #Opens file and either overwrites it or creates a new file
    if os.path.exists("test.csv"):
        #Overwrites
        toFile = open("test.csv", "w")
    else:
        #Creates new
        toFile = open("test.csv", "x")

    for song in userSet:
        #NOTE: song is URI now in this context, the key for "userSet"
        line_feature_selector(song, userSet[song], toFile)

    toFile.close()
    
    
    
 ### Some useful resources that helped us build the recommender: https://towardsdatascience.com/making-your-own-discover-weekly-f1ac7546fedb, https://medium.com/deep-learning-turkey/build-your-own-spotify-playlist-of-best-playlist-recommendations-fc9ebe92826a, https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b ###

CLIENT_ID = "76c240fd1a97458d9c1a3d77345c56c6"
CLIENT_SECRET = "fba5d3953c7c4ae28ffa16b9bc7e003f"

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

# SETTINGS 
endpoint_url = "https://api.spotify.com/v1/recommendations?"
user_id = "m9ttj2ay9q7b7banu1d7fquf9"

token = util.prompt_for_user_token( #change so the user can input their own info
        username=user_id,
        scope= "playlist-modify-public",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='http://localhost:8888/callback') #URI to the developer dashboard

spotify = spotipy.Spotify(auth=token) #client

user_top_genre = input("What genre have you been liking the most recently?: ")
user_top_artist = input("What about your most recent favorite artist?: ")
user_danceability = input("How much danceability do you want your recommended songs to have? A value of 0.0 is least danceable and 1.0 is most danceable: ")

#need to get artist ID so can feed into seed artist
artist_info = spotify.search(user_top_artist, type="artist", market="US", limit=1) #gets artist info so can find URI value
for item in artist_info['artists']['items']:
  artist_id = item['id'] #finds artist ID

# FILTERS
limit = 10
market = "US"
seed_genres= user_top_genre
seed_artists = artist_id
target_danceability = user_danceability
uris = []

# PERFORM THE QUERY
query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
query += f'&seed_artists={seed_artists}'

response = requests.get(query, 
               headers={"Content-Type":"application/json", 
                        "Authorization":f"Bearer {token}"})
json_response = response.json()

recommended_songs = [] #list of all recommended songs
like_or_dislike = {} #dict of all the songs and whether or not user likes or dislikes them
print('\nRecommended Songs:')
for i,j in enumerate(json_response['tracks']):
            uris.append(j['uri'])
            recommended_songs.append(f"{j['name']}\" by {j['artists'][0]['name']}") #appends each song
            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")

#creates playlist for recommended songs
new_playlist_name_for_rec = "Daily Song Recommender"
user_playlists = spotify.user_playlists(user_id) #gets all playlists of user
list_of_playlists = []

for playlist in user_playlists['items']:
    list_of_playlists.append(playlist['name'])

for name in list_of_playlists:
    if new_playlist_name_for_rec in list_of_playlists:
        break
    else:
        spotify.user_playlist_create(user=user_id, name=new_playlist_name_for_rec, public=True, collaborative=False, description="Recommended songs")  # creates the new playlist
        list_of_playlists.append(new_playlist_name_for_rec)

#finds playlist ID for newly created playlist - https://towardsdatascience.com/using-python-to-create-spotify-playlists-of-the-samples-on-an-album-e3f20187ee5e
rec_playlist_ID = ''
user_playlists_after_rec_added = spotify.user_playlists(user_id) #gets all playlists of user
for playlist in user_playlists_after_rec_added['items']:
    if playlist['name'] == new_playlist_name_for_rec:
        rec_playlist_ID = playlist['id'] #gets ID of new playlist

#adds all of the recommended songs to the newly created recommended playlist
spotify.user_playlist_add_tracks(user_id, rec_playlist_ID, uris)

print("\nAll recommended songs are in the Daily Song Recommender playlist. Give them a listen and come back to select your favorites :)")

#input the number by the song when prompted to ask which songs did you like
liked_songs = [str(song) for song in input("\nWhich songs did you like? (separate with a comma and space): ").split(', ')] #gets users input
#sets the users chosen songs to "like"
like_dislike_uri = {}

for like in liked_songs:
  like_dislike_uri[uris[int(like) -1 ]] = "l"
  like_or_dislike[recommended_songs[int(like) - 1]] = "like"

left_over_songs = [] #gets the songs that the user didnt chose - the ones they disliked
left_over_uris = [] #gets the uri's of the songs the user disliked
name_of_liked_songs = [] #gets list of the liked songs
uri_of_liked_songs = [] #gets the URI of the liked song
for like in liked_songs:
  uri_of_liked_songs.append(uris[int(like) - 1])
  name_of_liked_songs.append(recommended_songs[int(like) - 1]) 

#sets the disliked songs to "dislike" in the dict
for song in recommended_songs:
  if song not in name_of_liked_songs:
    left_over_songs.append(song) #list of disliked songs - in case we need it later on
    like_or_dislike[song] = "dislike"

#mimics the above behavior but uses URI instead of string identifiers. This allows me to extract features more easily.
for uri in uris:
    if uri not in uri_of_liked_songs:
        left_over_uris.append(uri)
        like_dislike_uri[uri] = "d"

#creates new playlist with songs that the user liked from the recommended list
new_playlist_name = input("What do you want your new playlist to be called?")
list_of_playlists_for_liked = []

for playlist in user_playlists['items']:
    list_of_playlists_for_liked.append(playlist['name'])

for name in list_of_playlists_for_liked:
    if new_playlist_name in list_of_playlists_for_liked:
        break
    else:
        spotify.user_playlist_create(user=user_id, name = new_playlist_name, public= True, collaborative= False, description= "Liked songs from recommended playlist") #creates the new playlist
        list_of_playlists_for_liked.append(new_playlist_name)

#finds playlist ID for newly created playlist - https://towardsdatascience.com/using-python-to-create-spotify-playlists-of-the-samples-on-an-album-e3f20187ee5e
new_playlist_ID = ''

user_playlists_after_liked_added = spotify.user_playlists(user_id) #gets all playlists of user
for playlist in user_playlists_after_liked_added['items']:
    if playlist['name'] == new_playlist_name:
        new_playlist_ID = playlist['id'] #gets ID of new playlist

spotify.user_playlist_add_tracks(user_id, new_playlist_ID, uri_of_liked_songs)

print("Your new playlist with all your liked songs is ready! Enjoy :)")

outputCSVTrain(like_dislike_uri)

user_top_artist = input("What is another recent favorite artist?: ")
user_danceability = input("How much danceability do you want your recommended songs to have? A value of 0.0 is least danceable and 1.0 is most danceable: ")

#need to get artist ID so can feed into seed artist
artist_info = spotify.search(user_top_artist, type="artist", market="US", limit=1) #gets artist info so can find URI value
for item in artist_info['artists']['items']:
  artist_id = item['id'] #finds artist ID

# FILTERS
limit = 10
market = "US"
seed_genres= user_top_genre
seed_artists = artist_id
target_danceability= user_danceability
uris = []

# PERFORM THE QUERY
query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
query += f'&seed_artists={seed_artists}'

response = requests.get(query,
               headers={"Content-Type":"application/json",
                        "Authorization":f"Bearer {token}"})
json_response = response.json()

recommended_songs = [] #list of all recommended songs
like_or_dislike = {} #dict of all the songs and whether or not user likes or dislikes them
print('\nRecommended Songs:')
for i,j in enumerate(json_response['tracks']):
            uris.append(j['uri'])
            recommended_songs.append(f"{j['name']}\" by {j['artists'][0]['name']}") #appends each song
            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")

#creates playlist for recommended songs
new_playlist_name_for_rec = "Daily Song Recommender 2"
user_playlists = spotify.user_playlists(user_id) #gets all playlists of user
list_of_playlists = []

for playlist in user_playlists['items']:
    list_of_playlists.append(playlist['name'])

for name in list_of_playlists:
    if new_playlist_name_for_rec in list_of_playlists:
        break
    else:
        spotify.user_playlist_create(user=user_id, name=new_playlist_name_for_rec, public=True, collaborative=False, description="Recommended songs")  # creates the new playlist
        list_of_playlists.append(new_playlist_name_for_rec)

#finds playlist ID for newly created playlist - https://towardsdatascience.com/using-python-to-create-spotify-playlists-of-the-samples-on-an-album-e3f20187ee5e
rec_playlist_ID = ''
user_playlists_after_rec_added = spotify.user_playlists(user_id) #gets all playlists of user
for playlist in user_playlists_after_rec_added['items']:
    if playlist['name'] == new_playlist_name_for_rec:
        rec_playlist_ID = playlist['id'] #gets ID of new playlist

#adds all of the recommended songs to the newly created recommended playlist
spotify.user_playlist_add_tracks(user_id, rec_playlist_ID, uris)

print("\nAll recommended songs are in the Daily Song Recommender 2 playlist. Give them a listen and come back to select your favorites :)")

#input the number by the song when prompted to ask which songs did you like
liked_songs = [str(song) for song in input("\nWhich songs did you like? (separate with a comma and space): ").split(', ')] #gets users input
#sets the users chosen songs to "like"
like_dislike_uri = {}

for like in liked_songs:
  like_dislike_uri[uris[int(like) -1 ]] = "l"
  like_or_dislike[recommended_songs[int(like) - 1]] = "like"

left_over_songs = [] #gets the songs that the user didnt chose - the ones they disliked
left_over_uris = [] #gets the uri's of the songs the user disliked
name_of_liked_songs = [] #gets list of the liked songs
uri_of_liked_songs = [] #gets the URI of the liked song
for like in liked_songs:
  uri_of_liked_songs.append(uris[int(like) - 1])
  name_of_liked_songs.append(recommended_songs[int(like) - 1])

#sets the disliked songs to "dislike" in the dict
for song in recommended_songs:
  if song not in name_of_liked_songs:
    left_over_songs.append(song) #list of disliked songs - in case we need it later on
    like_or_dislike[song] = "dislike"

#mimics the above behavior but uses URI instead of string identifiers. This allows me to extract features more easily.
for uri in uris:
    if uri not in uri_of_liked_songs:
        left_over_uris.append(uri)
        like_dislike_uri[uri] = "d"

#creates new playlist with songs that the user liked from the recommended list
new_playlist_name = input("What do you want your new playlist to be called?")
list_of_playlists_for_liked = []

for playlist in user_playlists['items']:
    list_of_playlists_for_liked.append(playlist['name'])

for name in list_of_playlists_for_liked:
    if new_playlist_name in list_of_playlists_for_liked:
        break
    else:
        spotify.user_playlist_create(user=user_id, name = new_playlist_name, public= True, collaborative= False, description= "Liked songs from recommended playlist") #creates the new playlist
        list_of_playlists_for_liked.append(new_playlist_name)

#finds playlist ID for newly created playlist - https://towardsdatascience.com/using-python-to-create-spotify-playlists-of-the-samples-on-an-album-e3f20187ee5e
new_playlist_ID = ''

user_playlists_after_liked_added = spotify.user_playlists(user_id) #gets all playlists of user
for playlist in user_playlists_after_liked_added['items']:
    if playlist['name'] == new_playlist_name:
        new_playlist_ID = playlist['id'] #gets ID of new playlist

spotify.user_playlist_add_tracks(user_id, new_playlist_ID, uri_of_liked_songs)

print("Your new playlist with all your liked songs is ready! Enjoy :)")

outputCSVTest(like_dislike_uri)


