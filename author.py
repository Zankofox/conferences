import streamlit as st
import config as cf
from utils import print_header, print_footer, dico_author, df_author_overview, df_video
from video import print_video_overview


def display_author(link_page, image_url, author_name, count_video):
    a = st.container(border=True)
    with a:
        st.markdown(
            f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>',
            unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
        <span style="font-weight: bold;">{author_name}</span>
        <span style="font-size: 14px;">({int(count_video)})</span>
        </div>
        """, unsafe_allow_html=True)

def print_author_overview():
    count_author = int(len(df_author_overview))
    st.markdown(f"""
            <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
            <span style="font-size: 38px;font-weight: bold;">Intervenants</span>
            <span style="font-size: 18px;">({count_author})</span>
            </div>
            """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(cf.AUTHOR_COL)
    counter = 0
    dico_author = df_author_overview.sort_values(by='count', ascending=False).set_index('author_id').to_dict(orient='index')

    for k, v in dico_author.items():
        link_page = f'/author_{k}'
        image_url = v['tn_link']
        author_name = v['author']
        count_video = v['count']
        if counter % cf.AUTHOR_COL == 0:
            with c1:
                display_author(link_page, image_url, author_name, count_video)
        if counter % cf.AUTHOR_COL == 1:
            with c2:
                display_author(link_page, image_url, author_name, count_video)
        if counter % cf.AUTHOR_COL == 2:
            with c3:
                display_author(link_page, image_url, author_name, count_video)
        counter += 1

def page_author(author_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    author_name = dico_author[author_id]['author']
    video_ids = list(df_video.loc[df_video['author'] == f'{author_name}', 'video_id'])

    # DISPLAY
    print_header()
    st.title(f'{author_name}')
    print_video_overview(video_ids, ignore_author=True)
    print_footer()