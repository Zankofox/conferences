import random

import streamlit as st
import config as cf
from utils import print_header, print_footer, df_video, df_tags_overview
from video import print_video_overview

def display_tag(link_page, image_url, tag_name, count_video):
    a = st.container(border=True)
    with a:
        st.markdown(
            f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>',
            unsafe_allow_html=True)
        st.markdown(f"""
                <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
                <span style="font-weight: bold;">{tag_name}</span>
                <span style="font-size: 14px;">({count_video})</span>
                </div>
                """, unsafe_allow_html=True)

def print_tag_overview():
    c1, c2, c3, c4 = st.columns(cf.TAG_COL)
    dico_col = {0: c1, 1: c2, 2: c3, 3: c4}
    counter = 0
    dico_tags = df_tags_overview.sort_values(by='count', ascending=False).set_index('tag_id').to_dict(orient='index')
    for k, v in dico_tags.items():
        link_page = f'/tag_{k}'
        image_url = v['tn_link']
        tag_name = v['tag']
        count_video = v['count']
        nombre = counter % cf.TAG_COL
        with dico_col[nombre]:
            display_tag(link_page, image_url, tag_name, count_video)
        counter += 1

def page_tag(tag_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    dico_tag = df_tags_overview.set_index('tag_id').to_dict(orient='index')
    tag_name = dico_tag[tag_id]['tag']
    video_ids = list(df_video.loc[
                         (df_video['tag1'] == f'{tag_name}') | (df_video['tag2'] == f'{tag_name}') | (
                                     df_video['tag3'] == f'{tag_name}') | (
                                     df_video['tag4'] == f'{tag_name}') | (
                                     df_video['tag5'] == f'{tag_name}'), 'video_id'])
    print_header()
    st.title(f'{tag_name}')
    random.shuffle(video_ids)
    print_video_overview(video_ids)
    print_footer()
