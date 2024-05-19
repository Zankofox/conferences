import pandas as pd
import streamlit as st
import utils

from pytube import YouTube
from datetime import datetime
import os
import shutil
today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':','-')

if 'video_id' not in st.session_state:
    st.session_state['video_id'] = 3
    st.session_state['link'] = 3
    st.session_state['name'] = 4
df = pd.DataFrame([st.session_state], index=[0])
a = 4



# df_video = utils.df_video
# a = st.text_input('super')
# user_data = {
#     'video_id': [a]}


x = 4
# dico_video = df_video[0:0].to_dict()
# for col in dico_video.keys():
#     dico_video[col] = 4
# #       st.button('Upload', on_click=update_input(df_video))
# df_new_row = pd.DataFrame(dico_video)
# original_df = ut.df_video
# final_df = pd.concat([original_df, new_df])
# x = 4




# df_video = pd.read_excel('conf.xlsx')
# dico_video = df_video.set_index('video_id').to_dict(orient='index')
# x = 4
# df = df_video
# dico_video = df.set_index('link').to_dict(orient='index')
# dico_video_updated_fill = {}
# dico_video_updated_override = {}
# for k, v in dico_video.items():
#     dico_temp_fill = dico_video[k].copy()


# def update_input(df):
#     video_ids = list(df['video_id'])
#     dico_video = df.set_index('video_id').to_dict(orient='index')
#     dico_video_updated_fill = {}
#     dico_video_updated_override = {}
#     for video_id in video_ids:
#         dico_temp_fill = dico_video[video_id].copy()
#         dico_temp_override = dico_video[video_id].copy()
#         link = dico_temp_fill['link']
#         yt = YouTube(link)
#         cols_to_check = {'date':
#                          'length': pd.to_datetime(yt.length, unit='s').time(),
#                          'name': yt.title,
#                          'tn_link': yt.thumbnail_url}
#         cols_to_ignore = list(cols_to_check.keys()) + ['video_id']
#         for k, v in cols_to_check.items():
#             dico_temp_override[k] = v
#             if (str(dico_temp_fill[k]) == 'nan') | (str(dico_temp_fill[k]) == 'NaT'):
#                 dico_temp_fill[k] = v
#         for col in [x for x in df_video.columns if x not in cols_to_ignore]:
#             dico_temp_fill[col] = dico_video[video_id][col]
#             dico_temp_override[col] = dico_video[video_id][col]
#
#         dico_video_updated_fill[video_id] = dico_temp_fill
#         dico_video_updated_override[video_id] = dico_temp_override
#
#     df_video_updated_fill = pd.DataFrame(dico_video_updated_fill).T
#     df_video_updated_fill['video_id'] = list(dico_video_updated_fill.keys())
#     df_video_updated_fill = df_video_updated_fill[['video_id'] + [x for x in df_video_updated_fill.columns if x !='video_id']]
#
#     df_video_updated_override = pd.DataFrame(dico_video_updated_override).T
#     df_video_updated_override['video_id'] = list(dico_video_updated_override.keys())
#     df_video_updated_override = df_video_updated_override[['video_id'] + [x for x in df_video_updated_override.columns if x != 'video_id']]
#
#     df_video_updated_fill.to_excel('conf_fill.xlsx', sheet_name='videos', index=False)
#     df_video_updated_override.to_excel('conf_override.xlsx', sheet_name='videos', index=False)
