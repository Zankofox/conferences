import pandas as pd
import streamlit as st
import config as cf
import random
from utils import print_header, print_footer, dico_author, df_video, df_rockstar, \
    df_quotes, get_quote_size, display_photo, get_cat_id_from_name, get_author_id_from_name
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
                <span style="font-size: 14px;">({count_video})</span>
                </div>
                """, unsafe_allow_html=True)

def display_rockstar(link_page, image_path, author_name):
    cat1_name = df_rockstar.loc[df_rockstar['rockstar'] == author_name, 'cat1'].values[0]
    cat1_id = get_cat_id_from_name(cat1_name)
    cat2_name = df_rockstar.loc[df_rockstar['rockstar'] == author_name, 'cat2'].values[0]
    a = st.container(border=True)
    with a:
        col1, col2 = st.columns([4, 2])
        with col1:
            display_photo(link_page, image_path)
        with col2:
            b = st.container(height=380, border=False)
            with b:
                quote = random.choice(list(df_quotes.loc[df_quotes['Author'] == author_name, 'Quote']))
                quote_size = get_quote_size(quote)
                st.markdown(f"""
                    <div style="
                        display: flex; 
                        justify-content: center;
                        align-items: center; 
                        height: 38vh; 
                        font-family: Nunito;
                        font-size: {quote_size}px; 
                        margin: 0; 
                        padding: 15;
                        font-style: italic;
                        text-align: center;
                    ">
                        "{quote}"
                    </div>
                """, unsafe_allow_html=True)
            cc1, cc2, cc3, cc4, cc5 = st.columns(5)
            with cc1:
                image_icone_path_1 = f'assets/categories/{cat1_name}.png'
                display_photo(f'/cat_{cat1_id}', image_icone_path_1, 80)
                st.markdown(f"""
                <div style="font-family: Lato; font-size: 24ddpx; padding-bottom: 8px;">
                <span style="font-weight: bold;padding-bottom: 8px;">{cat1_name}</span>
                </div>
            """, unsafe_allow_html=True)
            with cc5:
                if str(cat2_name) != 'nan':
                    cat2_id = get_cat_id_from_name(cat2_name)
                    image_icone_path_2 = f'assets/categories/{cat2_name}.png'
                    display_photo(f'/cat_{cat2_id}', image_icone_path_2, 80)
                    st.markdown(f"""
                    <div style="font-family: Lato; font-size: 24ddpx; padding-bottom: 10px;">
                    <span style="font-weight: bold;padding-bottom: 8px;">{cat2_name}</span>
                    </div>
                    """, unsafe_allow_html=True)

def print_rock_star():
    rock_stars = list(df_rockstar['rockstar'])
    random.shuffle(rock_stars)
    for rock_star in rock_stars:
        author_id = get_author_id_from_name(rock_star)
        link_page = f'/author_{author_id}'
        pic_name = rock_star.split()[-1].lower()
        image_path = f'assets/rockstars/final/{pic_name}.png'
        display_rockstar(link_page, image_path, rock_star)

def print_author_overview():
    counter = 0
    c1, c2, c3, c4 = st.columns(cf.AUTHOR_COL)
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
        if counter % cf.AUTHOR_COL == 3:
            with c4:
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
