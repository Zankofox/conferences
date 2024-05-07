import streamlit as st
import pandas as pd
import os
import wikipedia as wp
import conf_utils as uti
st.set_page_config(page_title='Conférences.fr', page_icon='🎈', layout='wide')

df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
dico_video = df_video.set_index('video_id').to_dict(orient='index')

def print_home():
    st.title('Conférences.fr')
    df_author = uti.get_df_author(df_video)
    df_tags = uti.get_df_tags(df_video)
    t1, t2 = st.tabs(['Intervenants', 'Themes'])
    with t1:
        print_author_overview(df_author)
    with t2:
        print_tag_overview(df_tags)

def main():
    all_videos = list(df_video['video_id'])
    print_home()
main()
