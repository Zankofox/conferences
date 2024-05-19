import streamlit as st
from datetime import datetime
import os
from utils import move_and_rename_file_if_exists, check_and_delete_file
import pandas as pd
from pytube import YouTube
st.set_page_config(page_title='Conférences.fr', page_icon='⚙', layout='wide')
today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':','-')
df_video = pd.read_excel('input.xlsx')
max_id = max(df_video['video_id']) + 1

def fetch_data_youtube():
    a = st.text_input('YOUTUBE LINK')
    if a !='':
        st.session_state.ytlink = a
    st.button('GET DATA')
def add_video():
    if 'ytlink' not in st.session_state:
        fetch_data_youtube()
    else:
        with st.form('user_data', clear_on_submit=True):
            st.session_state.yt = YouTube(st.session_state.ytlink)
            st.session_state.go = False
            yt = st.session_state.yt
            video_id = st.number_input('video_id', value=max_id, key="video_id")
            link = st.text_input('link', value=st.session_state.ytlink, key="link")
            name = st.text_input('name', value=yt.title, key="name")
            author = st.text_input('author', key="author")
            video_type = st.text_input('type', key="type")
            tag1 = st.text_input('tag1', key="tag1")
            tag2 = st.text_input('tag2', key="tag2")
            tag3 = st.text_input('tag3', key="tag3")
            tag4 = st.text_input('tag4', key="tag4")
            startTimeCode = st.text_input('startTimeCode', key="startTimeCode")
            questionsTimeCode = st.text_input('questionsTimeCode', key="questionsTimeCode")
            audioQuality = st.text_input('audioQuality', key="audioQuality")
            videoQuality = st.text_input('videoQuality', key="videoQuality")
            length = st.text_input('length', value=pd.to_datetime(yt.length, unit='s').time(), key="length")
            publish_date = st.date_input('publish_date', value=pd.Timestamp(yt.publish_date), key="publish_date")
            tn_link = st.text_input('tn_link', value=yt.thumbnail_url, key="tn_link")
            a = st.form_submit_button('Submit')
            if a:
                user_data = {
                    'video_id': video_id,
                    'link': link,
                    'name': name,
                    'author': author,
                    "type": video_type,
                    'tag1': tag1,
                    'tag2': tag2,
                    'tag3': tag3,
                    'tag4': tag4,
                    'startTimeCode': startTimeCode,
                    'questionsTimeCode': questionsTimeCode,
                    'audioQuality': audioQuality,
                    'videoQuality': videoQuality,
                    'length': length,
                    'publish_date': publish_date,
                    'tn_link': tn_link
                }
                df = pd.DataFrame([user_data], index=[0])
                df.to_excel('df_temp.xlsx')
        if os.path.exists('df_temp.xlsx'):
            df_temp = pd.read_excel('df_temp.xlsx')
            final_df = pd.concat([df_video, df_temp])
            move_and_rename_file_if_exists('input.xlsx', 'archive_input', f'input_archive_{today}.xlsx')
            final_df.to_excel('input.xlsx', index=False)
            st.success('Conférence ajoutée !')
            check_and_delete_file('df_temp.xlsx')
            st.write(df)
            st.write(final_df.sort_values(by='video_id', ascending=False))


add_video()