import pandas as pd
import streamlit as st
import config as cf
from utils import print_footer, print_header, get_max_len, get_sec_from_tc, print_tags, df_video, dico_video

def display_video(link_page, image_url, video_name):
    # a = st.container(height=380, border=False)
    # with a:
    video_short_name = video_name[:45] + '...'
    if len(video_name) < 48:
        video_short_name = video_name
    st.markdown(f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{cf.IMAGE_WIDTH_PERCENT}%;height:auto;"></a>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-family: Tahoma; font-size: 20px; font-weight: bold;" title="{video_name}">{video_short_name}</p>', unsafe_allow_html=True)

def print_video_overview(video_ids, ignore_author=False):
    c1, c2, c3 = st.columns(cf.VIDEO_COL)
    counter = 0
    dico_col = {0: c1, 1: c2, 2: c3}
    df_ids = pd.DataFrame({'id': video_ids, 'row': [int(x / 3) + 1 for x in range(len(video_ids))]})
    for row in list(set(df_ids['row'])):
        row_ids = list(df_ids.loc[df_ids['row'] == row, 'id'])
        max_len = get_max_len(row_ids)

        if max_len > 65:
            height = 55
        else:
            height = 30
        for video_id in row_ids:
            nombre = counter % cf.VIDEO_COL
            dico_video_temp = dico_video[video_id]
            link_page = f'/video_{video_id}'
            image_url = dico_video_temp['tn_link']
            video_name = dico_video_temp['name']
            with dico_col[nombre]:
                a = st.container(border=True)
                with a:
                    display_video(link_page, image_url, video_name)
                    print_tags(video_id, height, ignore_author)
                counter += 1

def page_video(video_id):
    st.set_page_config(page_title='Conférences.fr', page_icon= '💡', layout='wide')
    dico_video_temp = dico_video[video_id]
    author = dico_video_temp['author']
    name = dico_video_temp['name']
    tags = [x for x in [dico_video_temp['tag1'], dico_video_temp['tag2'], dico_video_temp['tag3']] if str(x) != 'nan']
    stc = dico_video_temp['startTimeCode']
    qtc = dico_video_temp['questionsTimeCode']
    link = dico_video_temp['link']
    video_overview_ids = list(df_video.loc[
                                  (df_video['author'] == author) | (df_video['tag1'].isin(tags)) | (
                                      df_video['tag2'].isin(tags)) | (
                                      df_video['tag3'].isin(tags)), 'video_id'])
    if video_id in video_overview_ids:
        video_overview_ids.remove(video_id)
    print_header()
    with st.container(border=False):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(
                f'''<p style="font-size:36px; text-align:left; font-family:Tahoma;"><strong>''' + name + '''</strong></p>''',
                unsafe_allow_html=True)
    print_tags(video_id, height=25)

    with st.container():
        a = st.empty()
        with a:
            st.video(link)
        # BUTTONS
        if (str(stc) != 'nan') & (str(qtc) != 'nan'):
            c1, c2 = st.columns(2)
            with c1:
                if str(stc) != 'nan':
                    if st.button('Début de la conférence', use_container_width=True):
                        skip_time = get_sec_from_tc(pd.to_datetime(stc))
                        with a:
                            st.video(link, start_time=skip_time, autoplay=True)
            with c2:
                if str(qtc) != 'nan':
                    if st.button("Passer aux questions", use_container_width=True):

                        skip_time = get_sec_from_tc(pd.to_datetime(qtc))
                        with a:
                            st.video(link, start_time=skip_time, autoplay=True)

        if (str(stc) != 'nan') & (str(qtc) == 'nan'):
            if str(stc) != 'nan':
                if st.button('Début de la conférence', use_container_width=True):
                    skip_time = get_sec_from_tc(pd.to_datetime(stc))
                    with a:
                        st.video(link, start_time=skip_time, autoplay=True)
        st.markdown(
            """
        <style>
        button {
            height: 60px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    with st.container():
        st.header('Conférences connexes')
        st.markdown(' ')
        print_video_overview(video_overview_ids)
        print_footer()
