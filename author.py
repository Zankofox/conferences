import streamlit as st
import conf_utils as cf
import overview as ov
import pandas as pd

def page_author(author_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
    dico_video = df_video.set_index('video_id').to_dict(orient='index')
    df_author = cf.get_df_author(df_video)
    dico_author = df_author.set_index('author_id').to_dict(orient='index')
    author_name = dico_author[author_id]['author']
    video_ids = list(df_video.loc[df_video['author']==f'{author_name}', 'video_id'])
    cf.print_header()
    st.title(f'{author_name}')
    ov.print_video_overview(video_ids, ignore_author=True)