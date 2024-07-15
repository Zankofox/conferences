import streamlit as st
import config as cf
import random
from utils import print_header, print_footer, df_video, df_cat_overview, display_menu, get_cat_id_from_name
from video import print_video_overview

def display_cat(link_page, image_url, cat_name, count_video):
    a = st.container(border=True)
    with a:
        st.markdown(
            f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>',
            unsafe_allow_html=True)
        st.markdown(f"""
                <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
                <span style="font-weight: bold;">{cat_name}</span>
                <span style="font-size: 14px;">({count_video})</span>
                </div>
                """, unsafe_allow_html=True)
@st.cache_resource(ttl='10m')
def print_cat_overview():
    c1, c2, c3 = st.columns(cf.CAT_COL)
    counter = 0
    dico_col = {0: c1, 1: c2, 2: c3}
    dico_cats = df_cat_overview.sort_values(by='cat', ascending=True).set_index('cat_id').to_dict(orient='index')
    for k, v in dico_cats.items():
        cat_name = v['cat']
        if cat_name in ['Interview']:
            continue
        link_page = f'/cat_{k}'
        image_path = f'assets/categories/{cat_name}.png'
        count_cat = v['count']
        nombre = counter % cf.CAT_COL
        with dico_col[nombre]:
            a = st.container(border=True)
            with a:
                display_menu(link_page, image_path, cat_name, count_cat)
        counter += 1

def page_cat(cat_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    dico_cat = df_cat_overview.set_index('cat_id').to_dict(orient='index')
    cat_name = dico_cat[cat_id]['cat']
    video_ids = list(df_video.loc[(df_video['cat1'] == f'{cat_name}') | (df_video['cat2'] == f'{cat_name}'), 'video_id'])
    print_header()
    c1,c2 = st.columns([1,20])
    with c1:
        st.image(f'assets/categories/{cat_name}.png', width=80)
    with c2:
        st.title(f'{cat_name}')
    random.shuffle(video_ids)
    print_video_overview(video_ids)
    print_footer()
