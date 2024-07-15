import pandas as pd
import os
import streamlit as st
from datetime import datetime


from pytube import YouTube
from utils import move_and_rename_file_if_exists, check_and_delete_file

# st.set_page_config(page_title='Conférences.fr', page_icon='⚙', layout='wide')
today = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':','-')
df_video = pd.read_excel('input.xlsx')
max_id = max(df_video['video_id']) + 1
path = 'assets/categories'
filenames = next(os.walk(path), (None, None, []))[2]
categories2 = [x.replace('.png','') for x in filenames]
def fetch_data_youtube():
    a = st.text_input('YOUTUBE LINK')
    if a !='':
        st.session_state.ytlink = a
    st.button('GET DATA')

def add_video():
    st.title('Ajoute une conférence bro !')
    if 'ytlink' not in st.session_state:
        fetch_data_youtube()
    else:
        go = True
        with st.form('user_data', clear_on_submit=True):
            st.session_state.yt = YouTube(st.session_state.ytlink)
            st.session_state.go = False
            yt = st.session_state.yt
            video_id = st.number_input('video_id', value=max_id, key="video_id")
            link = st.text_input('link', value=st.session_state.ytlink, key="link")
            name = st.text_input('name', value=yt.title, key="name")
            author = st.text_input('author', key="author")
            video_type = st.text_input('type', value='Conférence', key="type")
            ranking = st.text_input('ranking', value = 5, key='ranking')
            cat1 = st.selectbox(label='Categorie 1', options= categories2, key='c1')
            cat2 = st.selectbox(label='Categorie 2',options= categories2, key='c2')
            tag1 = st.text_input('tag1', key="tag1")
            tag2 = st.text_input('tag2', key="tag2")
            tag3 = st.text_input('tag3', key="tag3")
            tag4 = st.text_input('tag4', key="tag4")
            tag5 = st.text_input('tag5', key="tag5")
            startTimeCode = st.text_input('startTimeCode', key="startTimeCode", value = '00:00:00')
            questionsTimeCode = st.text_input('questionsTimeCode', key="questionsTimeCode")
            audioQuality = st.selectbox(label='Audio Quality', options=['High', 'Medium', 'Low'],  key="audioQuality")
            videoQuality = st.selectbox(label='Video Quality', options=['High', 'Medium', 'Low'],  key="videoQuality")
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
                    "cat1" : cat1,
                    "cat2" : cat2,
                    "ranking" : ranking,
                    'tag1': tag1,
                    'tag2': tag2,
                    'tag3': tag3,
                    'tag4': tag4,
                    'tag5' : tag5,
                    'startTimeCode': startTimeCode,
                    'questionsTimeCode': questionsTimeCode,
                    'audioQuality': audioQuality,
                    'videoQuality': videoQuality,
                    'length': length,
                    'publish_date': publish_date,
                    'tn_link': tn_link
                }
                df = pd.DataFrame([user_data], index=[0])
                if df['name'][0] in (list(df_video['name'])):
                    go = False
                    st.error('Video already present')

                for col in [x for x in user_data.keys() if x not in ['questionsTimeCode', 'tag2', 'tag3', 'tag4','tag5', 'cat2']]:
                    if df[col][0] == '':
                        st.error(f'{col} cannot be empty !')
                        go = False

                if go:
                    df.to_excel('df_temp.xlsx')
                else:
                    st.stop()
        if os.path.exists('df_temp.xlsx'):
            df_temp = pd.read_excel('df_temp.xlsx')
            for col_to_remove in ['Unnamed: 0', 'categorie1', 'categorie2']:
                if col_to_remove in df_temp.columns:
                    df_temp = df_temp.drop(columns=col_to_remove)
            final_df = pd.concat([df_video, df_temp])
            move_and_rename_file_if_exists('input.xlsx', 'archive_input', f'input_archive_{today}.xlsx')
            final_df.to_excel('input.xlsx', index=False)
            st.success('Conférence ajoutée !')
            check_and_delete_file('df_temp.xlsx')
            st.write(df.T)
            # st.write(final_df.sort_values(by='video_id', ascending=False))
add_video()