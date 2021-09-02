# --- The MIT License (MIT) Copyright (c) Jacques Spectre (jacques.spectre@outlook.com), Wed Aug 25 21:58pm 2021 ---
# Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
# api_key = "Please set your own API key"
# channel_id = "Please set the channel_id you want to look for playlist videos_IDs"
import googleapiclient.discovery
import googleapiclient.errors
import json

channel_id = "UC45i13dEfEVac2IEJT_Nr5Q"

def getPlaylistVideosIDs(api_key, channel_id):
    api_service_name = "youtube"
    api_version = "v3"
    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()
    # Response for channel List
    if not response:
        return
    totalResults = response['pageInfo'].get('totalResults', None)
    if not totalResults:
        return
    if totalResults != 1:
        print('Need further check because totalResults is grater than 1.')
        return
    # Get video Lists from playlist_id
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    title = None
    nextPageToken = True
    videos_IDs = []
    while nextPageToken:
        if isinstance(nextPageToken, bool):
            request = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50)
        else:
            request = youtube.playlistItems().list(pageToken=nextPageToken, part='snippet', playlistId=playlist_id,
                                                   maxResults=50)
        response = request.execute()
        if not response:
            print('Requesting youtube.playlistItems.list has no response. Exit the loop.')
            break
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
    return videos_IDs, title

if __name__ == "__main__":
    with open('./.apikeys/gworkspace_api_key.ini', 'r', encoding='utf-8-sig') as f:
        api_key = f.read()
    videos_IDs, title = getPlaylistVideosIDs(api_key=api_key, channel_id=channel_id)
    if videos_IDs:
        print('saving videoIds...', end='')
        filename = title if title else channel_id
        with open(filename+'.json', 'w', encoding='utf-8-sig') as f:
            json.dump(videos_IDs, f, ensure_ascii=False, indent=2)
        print('Done.', end='')
