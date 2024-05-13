import streamlit as st
import utils as ut
import config as cf
import video as vid

def display_author(link_page, image_url, author_name, count_video):
    a = st.container(border=True)
    with a:
        st.markdown(
            f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>',
            unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
        <span style="font-weight: bold;">{author_name}</span>
        <span style="font-size: 18px;">({count_video})</span>
        </div>
        """, unsafe_allow_html=True)

def print_author_overview():
    st.title('Intervenants')
    c1, c2, c3 = st.columns(cf.AUTHOR_COL)
    counter = 0
    for author_id in list(ut.df_author['author_id']):
        dico_author_temp = ut.dico_author[author_id]
        link_page = f'/author_{author_id}'
        image_url = dico_author_temp['tn_link']
        author_name = dico_author_temp['author']
        count_video = dico_author_temp['count']
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
    author_name = ut.dico_author[author_id]['author']
    video_ids = list(ut.df_video.loc[ut.df_video['author'] == f'{author_name}', 'video_id'])

    # DISPLAY
    ut.print_header()
    st.title(f'{author_name}')
    vid.print_video_overview(video_ids, ignore_author=True)