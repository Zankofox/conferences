import streamlit as st
import conf_utils as cf
import pandas as pd
import overview as ov

def page_tag(tag_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
    dico_video = df_video.set_index('video_id').to_dict(orient='index')
    df_tag = cf.get_df_tags(df_video)
    dico_tag = df_tag.set_index('tag_id').to_dict(orient='index')
    tag_name = dico_tag[tag_id]['tag']
    video_ids = list(df_video.loc[(df_video['tag1']==f'{tag_name}') | (df_video['tag2']==f'{tag_name}')|(df_video['tag3']==f'{tag_name}'), 'video_id'])
    cf.print_header()
    st.title(f'{tag_name}')
    ov.print_video_overview(video_ids)
