import googleapiclient.discovery
import pandas as pd
import json

def get_api_key():
    with open('api_key.ini', 'r', encoding='utf-8-sig') as f:
        return f.read()

def create_clickable_id(id_list):
    url_template=''
    for id in id_list:
        url_template+='<a href="{id}" target="_blank">{id}</a><br>'.format(id=id)
    return url_template

with open('brothers_fq.json', 'r', encoding='utf-8-sig') as f:
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
fq.reset_index(inplace=True, drop=True)
fq['video_id'] = fq['videoId'].str[32:]
fq.to_html('my_1st.html', render_links=True)

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
alldf.drop(columns=['defaultAudioLanguage', 'thumbnails', 'liveBroadcastContent', 'channelId', 'localized', 'title', 'publishedAt'], inplace=True)
fq = fq.merge(alldf)
fq.sort_values('publishedAt', inplace=True, ascending=False)
fq.reset_index(inplace=True, drop=True)
#fq['urls'] = fq.description.str.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
#fq['href_urls'] = fq['urls'].apply(create_clickable_id)
fq['description'] = fq['description'].str.replace(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", r'<a href="\1" target="_blank">\1</a>', regex=True)
fq.drop(columns=['video_id', 'channelTitle'], inplace=True)
fq.to_html('my_2nd.html', render_links=True, escape=False)