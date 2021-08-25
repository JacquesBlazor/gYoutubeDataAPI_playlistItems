# --- The MIT License (MIT) Copyright (c) Jacques Spectre (jacques.spectre@outlook.com), Wed Aug 25 22:31pm 2021 ---
# Please get your own Google Youtube Data API key from https://console.developers.google.com/apis/credentials
# api_key = "Please set your own API key"
# the .json file was created by youtube_api_key_example3.py
import googleapiclient.discovery
from datetime import datetime
import pandas as pd
import json

def get_api_key():
    with open('./gSuite_ApiKey/api_key.ini', 'r', encoding='utf-8-sig') as f:
        return f.read()

def create_clickable_id(id_list):
    url_template=''
    for id in id_list:
        url_template+='<a href="{id}" target="_blank">{id}</a><br>'.format(id=id)
    return url_template

with open('柴鼠兄弟 ZRBros.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
df = pd.DataFrame(data)

for i, j in df[~df['title'].str.contains(r'[ | |｜│]', regex=True)].iterrows():
    df.loc[i]['title'] = df.loc[i]['title'] + '|沒有分類'
df[['title','category']] = df['title'].str.split(pat=r'\｜|\||\||\│', n=1, expand=True)
for i, j in df[df.category.isna()].iterrows():
    df.loc[i]['category'] = '沒有分類'
df['thumbnails'] = df['thumbnails'].apply(lambda lt: lt[-1])
df.sort_values('category', inplace=True)

fq = df[df['category'].str.contains('FQ')].copy()
fq['video_id'] = fq['videoId'].str[32:]
fq.reset_index(inplace=True, drop=True)

fq_videos = fq['video_id'].to_list()
quotient = len(fq_videos) // 23
alldf = pd.DataFrame()
api_key = get_api_key()
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
for i in range(quotient):
    data = []
    request = youtube.videos().list(part="snippet", id=",".join(j for j in fq_videos[i*23:i*23+23]))
    response = request.execute()
    for item in response['items']:
        data_dict = item['snippet'].copy()
        data_dict['video_id'] = item['id']
        data.append(data_dict)
    df = pd.DataFrame(data)
    alldf = pd.concat([df, alldf])
alldf.drop(columns=['defaultAudioLanguage', 'thumbnails', 'liveBroadcastContent', 'channelId', 'localized', 'title', 'publishedAt', 'channelTitle'], inplace=True)
fq = fq.merge(alldf)
fq.drop(columns=['video_id'], inplace=True)
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
fq['description'] = fq['description'].str.replace('|'.join(To_remove_lst), '', regex=True)
fq['description'] = fq['description'].str.replace(r"(https?://[-A-Za-z0-9+@#/%?=~_|!:,.;]*[-A-Za-z0-9+@#/%=~_|])", r'<a href="\1" target="_blank">\1</a>', regex=True)
fq['description'] = fq['description'].str.strip()
fq['description'] = fq['description'].str.replace(r"\n{3,}", '', regex=True)
fq['description'] = fq['description'].str.replace(r"\n", '<br>', regex=True)
fq.sort_values('publishedAt', inplace=True, ascending=False)
fq['publishedAt'] = fq['publishedAt'].apply(lambda x: datetime.fromisoformat(x[:-1]).strftime("%b-%u-%Y/%a%H:%M%p"))

fq.rename(columns={'title': '標題', 'videoId': '網址', 'publishedAt': '發佈日期', 'thumbnails': '封面圖片', 'category': '分類', 'description': '影片說明', 'tags': '標籤', 'categoryId': '號'}, inplace=True)
fq.set_index('發佈日期', inplace=True, drop=True)

pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')
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

with open('ZRBrosFQ.html', 'w', encoding='utf-8-sig') as f:
    f.write(html_string.format(table=fq.to_html(classes='mystyle', index_names=False, render_links=True, escape=False)))
