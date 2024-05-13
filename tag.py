import streamlit as st
import utils as ut
import config as cf
import video as vid

def display_tag(link_page, image_url, tag_name, count_video):
    a = st.container(border=True)
    with a:
        st.markdown(
            f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>',
            unsafe_allow_html=True)
        st.markdown(f"""
                <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
                <span style="font-weight: bold;">{tag_name}</span>
                <span style="font-size: 18px;">({count_video})</span>
                </div>
                """, unsafe_allow_html=True)


def print_tag_overview():
    st.title('Thèmes')
    c1, c2, c3, c4 = st.columns(cf.TAG_COL)

    counter = 0
    for tag_id in list(ut.df_tags['tag_id']):
        dico_tag_temp = ut.dico_tag[tag_id]
        link_page = f'/tag_{tag_id}'
        image_url = dico_tag_temp['tn_link']
        tag_name = dico_tag_temp['tag']
        count_video = dico_tag_temp['count']

        if counter % cf.TAG_COL == 0:
            with c1:
                display_tag(link_page, image_url, tag_name, count_video)
        if counter % cf.TAG_COL == 1:
            with c2:
                display_tag(link_page, image_url, tag_name, count_video)
        if counter % cf.TAG_COL == 2:
            with c3:
                display_tag(link_page, image_url, tag_name, count_video)
        if counter % cf.TAG_COL == 3:
            with c4:
                display_tag(link_page, image_url, tag_name, count_video)

        counter += 1

def page_tag(tag_id):
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    df_tag = ut.get_df_tags(ut.df_video)
    dico_tag = df_tag.set_index('tag_id').to_dict(orient='index')
    tag_name = dico_tag[tag_id]['tag']
    video_ids = list(ut.df_video.loc[(ut.df_video['tag1']==f'{tag_name}') | (ut.df_video['tag2']==f'{tag_name}')|(ut.df_video['tag3']==f'{tag_name}'), 'video_id'])
    ut.print_header()
    st.title(f'{tag_name}')
    vid.print_video_overview(video_ids)
