import googleapiclient.discovery
import googleapiclient.errors
import json

def getPlaylistVideosIDs(api_key, playlist_id="UUMUnInmOkrWN4gof9KlhNmQ"):
    videos_IDs = []
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50)
    response = request.execute()
    if response:
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

        return videos_IDs

if __name__ == "__main__":
    # Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
    api_key = "Please set your own API key"
    response = getPlaylistVideosIDs(api_key=api_key)
    if response:
        print('saving videoIds...', end='')
        with open('Mr & Mrs Gao.json', 'w', encoding='utf-8-sig') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        print('Done.', end='')
