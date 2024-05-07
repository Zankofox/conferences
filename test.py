import pandas as pd
import conf_utils as cf
from pytube import YouTube
from datetime import datetime

df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
dico_video = df_video.set_index('video_id').to_dict(orient='index')
df_tags = cf.get_df_tags(df_video)

def update_input(df_video):
    video_ids = list(df_video['video_id'])
    dico_video = df_video.set_index('video_id').to_dict(orient='index')
    dico_video_updated_fill = {}
    dico_video_updated_override = {}
    for video_id in video_ids:
        dico_temp_fill = dico_video[video_id].copy()
        dico_temp_override = dico_video[video_id].copy()
        link = dico_temp_fill['link']
        yt = YouTube(link)
        cols_to_check = {'date': pd.Timestamp(yt.publish_date),
                         'length': pd.to_datetime(yt.length, unit='s').time(),
                         'name': yt.title,
                         'tn_link': yt.thumbnail_url}
        cols_to_ignore = list(cols_to_check.keys()) + ['video_id']
        for k, v in cols_to_check.items():
            dico_temp_override[k] = v
            if (str(dico_temp_fill[k]) == 'nan') | (str(dico_temp_fill[k]) == 'NaT'):
                dico_temp_fill[k] = v
        for col in [x for x in df_video.columns if x not in cols_to_ignore]:
            dico_temp_fill[col] = dico_video[video_id][col]
            dico_temp_override[col] = dico_video[video_id][col]

        dico_video_updated_fill[video_id] = dico_temp_fill
        dico_video_updated_override[video_id] = dico_temp_override

    df_video_updated_fill = pd.DataFrame(dico_video_updated_fill).T
    df_video_updated_fill['video_id'] = list(dico_video_updated_fill.keys())
    df_video_updated_fill = df_video_updated_fill[['video_id'] + [x for x in df_video_updated_fill.columns if x !='video_id']]

    df_video_updated_override = pd.DataFrame(dico_video_updated_override).T
    df_video_updated_override['video_id'] = list(dico_video_updated_override.keys())
    df_video_updated_override = df_video_updated_override[['video_id'] + [x for x in df_video_updated_override.columns if x != 'video_id']]

    df_video_updated_fill.to_excel('conf_fill.xlsx', sheet_name='videos', index=False)
    df_video_updated_override.to_excel('conf_override.xlsx', sheet_name='videos', index=False)


stc = dico_video[1]['startTimeCode']
qtc = dico_video[1]['questionsTimeCode']
a = cf.get_sec_from_tc(pd.to_datetime(stc))
x = 4


# update_input(df_video)
