import requests
import urllib.parse
import urllib.request
import youtube_dl
from googleapiclient.discovery import build


def youtube_playlist():
    songs_added = []
    songs_not_added = []
    while True:
        try:
            url = input("Enter the URL\n>>> ").split('list=')[-1]
            request = youtube.playlistItems().list(
                part="id,snippet",
                playlistId=url,
                maxResults=500
            )
            response = request.execute()

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                youtube_url = f'https://www.youtube.com/watch?v={video_id}'
                video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
                    youtube_url, download=False
                )
                artist = video['artist']
                track = video['track']
                if artist is not None and track is not None:
                    songs_not_added.append(f'{artist} {track}')
                elif artist is None and track is None:
                    songs_added.append(video_title)
                spotify_search(track, artist, video_title)
            print(
                f'{len(songs_added) + len(songs_not_added)} Songs parsed in total!\n{len(songs_added)} Songs were added\n{len(songs_not_added)} Songs were NOT added')
            stats(songs_not_added, songs_added)
        except:
            print("Not a valid link")


def youtube_video():
    while True:
        try:
            url = input("What is the URL\n>>> ")
            video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
                url, download=False
            )
            artist = video['artist']
            track = video['track']
            title = None
            spotify_search(artist, track, title)
        except:
            print("Link not valid!")


def spotify_search(track, artist, title):
    query = urllib.parse.quote(f'{artist} {track}')
    parse_url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(
        parse_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_api}"
        }
    )
    response_json = response.json()
    results = response_json['tracks']['items']
    if results:
        if artist is None and track is None:
            print(f"No song found for {title}")
        else:
            print(f'Song Added: {artist}: {track}')
            song_id = results[0]['id']
            spotify_add(song_id)

    else:
        print(f"No song found for {artist}: {track}")


def spotify_add(song_id):
    parse_url = "https://api.spotify.com/v1/me/tracks"
    requests.put(
        parse_url,
        json={
            "ids": [song_id]
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_api}"
        }
    )


def main():
    while True:
        choice = input("What would you like to do:\n1) Add a playlist\n2) Add a Song\n3) Quit\n>>> ")
        if choice == '1':
            youtube_playlist()
        elif choice == '2':
            youtube_video()
        elif choice == '3':
            quit()
        else:
            print("Try again")


def manual_add(songs_not_added):
    score = 1
    for i in songs_not_added:
        print(f"{score}) {i}")
        artist = input("artist name\n>>> ")
        track = input("song name\n>>> ")
        title = i
        spotify_search(track, artist, title)
        score += 1


def stats(songs_added, songs_not_added):
    choice = input("What would you like to do:\n    1) Go to main menu\n    2) View songs Not added"
                   "\n    3) View songs added\n    4) Quit\n>>> ")
    if choice == '1':
        main()
    elif choice == '2':
        print('Songs NOT added:')
        for i in songs_not_added:
            print(f'    > {i}')
        inp = input("Would you like to add the songs not added manually? (y/n)\n>>> ").lower()
        if inp == "y":
            manual_add(songs_not_added)
        elif inp == "n":
            stats(songs_added, songs_not_added)
        else:
            print("Not understood taking back to the main menu")
            stats(songs_added, songs_not_added)
    elif choice == '3':
        print('Songs added:')
        for i in songs_added:
            print(f'    > {i}')
        stats(songs_added, songs_not_added)
    elif choice == '4':
        quit()
    else:
        print("Try again")
        stats(songs_added, songs_not_added)


if __name__ == '__main__':
    spotify_api = 'BQAAcOY86Br7Q3KK8Vlcf2fo9BBRj6PXlkln9E-SEv1uSBbLHXyeZKvn5xZXbrSbghDPTNiTYFdtkEdA1t_LD6UsB3V0Y3TS5IaSmMJKSJh4OOXYGuQ3EqZCYldGWkiPpJp2wdfGAtdRoMvgdnieB8nQy50RuV0uubBh0T5oxK528FmZMvGKb7wh8Y1bNy7KPV48prflHmBABSJ2ZHsdaeGRLI-AGxZ-QmelLXCJ0RTemWqU7oHkyuNPK0YR'
    youtube_api = 'AIzaSyC-61NQN3MNKB8LK1MLc4go-VI-2o_eeGg'
    youtube = build('youtube', 'v3', developerKey=youtube_api)
    main()
