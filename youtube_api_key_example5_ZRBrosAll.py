# --- The MIT License (MIT) Copyright (c) Jacques Spectre (jacques.spectre@outlook.com), Fri Sep 2 16:38pm 2021 ---
# Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
# api_key = "Please set your own API key"
# channel_id = "Please set the channel_id you want to look for playlist videos_IDs"


# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
import pandas as pd
import json


# %%
channel_id = "UC45i13dEfEVac2IEJT_Nr5Q"


# %%
with open('./.apikeys/gworkspace_api_key.ini', 'r', encoding='utf-8-sig') as f:
    api_key = f.read()


# %%
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
    return videos_IDs, title


# %%
videos_IDs, title = getPlaylistVideosIDs(api_key=api_key, channel_id=channel_id)
print('title: ', title)
print('total [%s] videos_IDs: %s' % (len(videos_IDs), str(videos_IDs[0])))
print('columns(keys) in videos_IDs: ', videos_IDs[0].keys())


# %%
df = pd.DataFrame(videos_IDs)
df


# %%
df.index


# %%
type(df['title'])


# %%
df.columns


# %%
df['title']


# %%
for i in df.columns:
    print(type(df[i][0]))


# %%
myfilter = ~df['title'].str.contains(r'\｜|\||\||\│', regex=True)


# %%
df[myfilter]


# %%
index_list = df[myfilter].index
index_list


# %%
df.iloc[193]['title']


# %%
for i, j in df[myfilter].iterrows():
    df.loc[i]['title'] = df.loc[i]['title'] + '|沒有分類'
df.loc[index_list]


# %%
df[['title','category']] = df['title'].str.split(pat=r'\｜|\||\||\│', n=1, expand=True)
df


# %%
df[df.category.isna()]
# index_list = df[df.category.isna()].index


# %%
df['thumbnails'].loc[0]


# %%
type(df['thumbnails'].loc[0])


# %%
#df['thumbnails'] = df['thumbnails'].apply(lambda lt: lt[-1])
def get_last(column_list):
    return column_list[-1]


# %%
df['thumbnails'] = df['thumbnails'].apply(get_last)
df


# %%
print(type(df['thumbnails'].loc[0]))


# %%
fq= df[df['category'].str.contains('FQ')].copy()
fq


# %%
fq.sort_values('publishedAt', inplace=True, ascending=False)
fq.reset_index(inplace=True, drop=True)
fq


# %%
def get_video_description(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']['description']


# %%
fq['description'] = fq['videoId'].str[32:].apply(get_video_description)
fq


# %%
To_remove_lst = [
  '【跟著柴學FQ 做自己的提款機】',
  '⭐️博客來全館即時榜、商業書籍榜、7日/30日排行榜、新書排行榜冠軍',
  '⭐️2020上半年MOMO網路書店暢銷榜Top7', '➤博客來 https://reurl.cc/8GnRXy',
  '➤誠品 https://reurl.cc/Kkj5lq', '➤金石堂 https://reurl.cc/z8zLp6',
  '【不用花錢也可以贊助柴鼠】', 'https://youtu.be/DGV964Fks2s',
  '【訂閱柴鼠也是一種鼓勵】',
  'http://bit.ly/2INZTDI',
  '【柴鼠兄弟相關頻道】',
  'YouTube頻道 https://www.youtube.com/c/柴鼠兄弟ZRBros',
  'FB粉絲頁 https://www.facebook.com/zrbros',
  'IG https://www.instagram.com/zrbros/',
  '【聯絡柴鼠】',
  'e-mail：paike.cat@gmail.com',
  '⭐️出版三個月熱銷突破十刷三萬冊',
  '⭐️博客來全館即時榜、商業書籍榜、7日/30日排行榜、新書排行榜冠軍',
  '⭐️博客來2020上半年暢銷書籍榜Top10',
  '⭐️2020上半年MOMO網路書店暢銷榜Top7',
  '【柴鼠LINE貼圖】',
  'https://pse.is/LRUBU',
  '⭐️博客來全館即時榜、商業書籍榜、7日/30日暢銷榜、新書排行榜冠軍',
  '⭐️2020上半年MOMO網路書店暢銷榜Top7',
  '🍎博客來',
  'https://reurl.cc/8GnRXy',
  '🍎誠品',
  'https://reurl.cc/Kkj5lq',
  '🍎金石堂',
  'https://reurl.cc/z8zLp6',
  '⭐️2020誠品書店年度暢銷Top2',
  '⭐️博客來2020年度百大暢銷書榜Top8',
  '⭐️博客來2020年度暢銷書榜Top8',
  '⭐️連續12週\(4/2~6/24\)蟬聯誠品書店財經/商業暢銷榜冠軍',
  'bilibili https://space.bilibili.com/130090309',
  '愛奇藝 http://tw.iqiyi.com/u/1421309132',
  'https://ppt.cc/fUrThx'
  ]


# %%
fq['description'] = fq['description'].str.replace('|'.join(To_remove_lst), '', regex=True)
fq


# %%
fq['description'] = fq['description'].str.replace(r"(https?://[-A-Za-z0-9+@#/%?=~_|!:,.;]*[-A-Za-z0-9+@#/%=~_|])", r'<a href="\1" target="_blank">\1</a>', regex=True)
fq['description'][1]


# %%
fq['description'] = fq['description'].str.strip()
fq['description'] = fq['description'].str.replace(r"\n{3,}", '', regex=True)
fq['description'] = fq['description'].str.replace(r"\n", '<br>', regex=True)


# %%
fq['publishedAt'] = fq['publishedAt'].apply(lambda x: datetime.fromisoformat(x[:-1]).strftime("%b-%u-%Y"))
fq


# %%
fq.index += 1
fq.reset_index(inplace=True, drop=False)
fq.rename(columns={'index': '序', 'title': '標題', 'videoId': '網址', 'publishedAt': '發佈日期', 'thumbnails': '封面圖片', 'category': '分類', 'description': '影片說明', 'tags': '標籤', 'categoryId': '號'}, inplace=True)
fq.set_index('發佈日期', inplace=True)
fq


# %%
html_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTML Pandas Dataframe with CSS</title>
    <style>
    .mystyle {{
        font-size: 11pt;
        font-family: Arial;
        border-collapse: collapse;
        border: 1px solid silver;
    }}

    .mystyle th {{
        background: silver;
        padding: 5px;
    }}

    .mystyle td {{
        padding: 5px;
    }}

    .mystyle tr:nth-child(even) {{
        background: #E0E0E0;
    }}

    .mystyle tr:hover {{
        background: silver;
        cursor: pointer;
    }}
    </style>
    </head>
    <body>
        {table}
    </body>
</html>'''


# %%
with open('%s.html' % title, 'w', encoding='utf-8-sig') as f:
    f.write(html_string.format(table=fq.to_html(classes='mystyle', index_names=False, render_links=True, escape=False)))
print('檔案 [%s.html] 已存檔完成。' % title)


