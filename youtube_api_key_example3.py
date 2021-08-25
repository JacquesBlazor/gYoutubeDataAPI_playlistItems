# --- The MIT License (MIT) Copyright (c) alvinconstantine(alvin.constantine@outlook.com), Sun Aug 8 04:33am 2021 ---

import googleapiclient.discovery
import googleapiclient.errors
import json

def get_api_key():
    with open('./gSuite_ApiKey/api_key.ini', 'r', encoding='utf-8-sig') as f:
        return f.read()

def getPlaylistVideosIDs(api_key, channel_id):
    videos_IDs = []
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()

    # Response for channel List
    if not response:
        return
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    request = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50)
    response = request.execute()

    # Response for channel List
    title = None
    if response:
        nextPageToken = response.get('nextPageToken', None)
        for count, item in enumerate(response['items']):
            if not title:
                title = item['snippet'].get('channelTitle', None)
            if not title:
                title = item['snippet'].get('videoOwnerChannelTitle', None)
            video_item = {
                'title': item['snippet']['title'],
                'videoId': 'https://www.youtube.com/watch?v=' + item['snippet']['resourceId']['videoId'],
                'publishedAt': item['snippet']['publishedAt']
            }
            if 'snippet' in item and 'thumbnails' in item['snippet'] and item['snippet']['thumbnails'].items():
                thumbnails = []
                for style, details in item['snippet']['thumbnails'].items():
                    if details.get('url', None):
                        thumbnails.append(details['url'])
                if thumbnails:
                    video_item['thumbnails'] = thumbnails
            videos_IDs.append(video_item)
            print(len(videos_IDs), count, video_item['videoId'])

        while nextPageToken:
            request = youtube.playlistItems().list(pageToken=nextPageToken, part='snippet', playlistId=playlist_id, maxResults=50)
            response = request.execute()
            if not response:
                break
            nextPageToken = response.get('nextPageToken', None)
            for count, item in enumerate(response['items']):
                video_item = {
                    'title': item['snippet']['title'],
                    'videoId': 'https://www.youtube.com/watch?v=' + item['snippet']['resourceId']['videoId'],
                    'publishedAt': item['snippet']['publishedAt']
                }
                if 'snippet' in item and 'thumbnails' in item['snippet'] and item['snippet']['thumbnails'].items():
                    thumbnails = []
                    for style, details in item['snippet']['thumbnails'].items():
                        if details.get('url', None):
                            thumbnails.append(details['url'])
                    if thumbnails:
                        video_item['thumbnails'] = thumbnails
                videos_IDs.append(video_item)
                print(len(videos_IDs), count, video_item['videoId'])

        return videos_IDs, title

if __name__ == "__main__":
    # Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
    #api_key = "Please set your own API key"
    api_key = get_api_key()
    # channel_id = "Please set the channel_id you want to look for playlist videos_IDs"
    channel_id = "UC45i13dEfEVac2IEJT_Nr5Q"
    videos_IDs, title = getPlaylistVideosIDs(api_key=api_key, channel_id=channel_id)
    if videos_IDs:
        print('saving videoIds...', end='')
        filename = title if title else channel_id
        with open(filename+'.json', 'w', encoding='utf-8-sig') as f:
            json.dump(videos_IDs, f, ensure_ascii=False, indent=2)
        print('Done.', end='')
