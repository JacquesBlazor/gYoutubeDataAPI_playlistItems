import googleapiclient.discovery
import googleapiclient.errors
import json

if __name__ == "__main__":
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
    api_key = "Please set your own API key"
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId="UUMUnInmOkrWN4gof9KlhNmQ",
        maxResults=50
    )
    response = request.execute()

    print(response)

    # Save response object(dict) to a JSON file with indent as 2 and encoding as utf-8-sig
    with open('Mr & Mrs Gao.json_1', 'w', encoding='utf-8-sig') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
