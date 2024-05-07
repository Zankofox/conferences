import pandas as pd
import streamlit as st
import conf_utils as cf
import overview as ov

def page_video(video_id):
    st.set_page_config(page_title='Conférences.fr', layout='wide')
    df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
    dico_video = df_video.set_index('video_id').to_dict(orient='index')[video_id]
    author = dico_video['author']
    name = dico_video['name']
    tags = [x for x in [dico_video['tag1'], dico_video['tag2'], dico_video['tag3']] if str(x) != 'nan']
    stc = dico_video['startTimeCode']
    qtc = dico_video['questionsTimeCode']
    link = dico_video['link']
    video_overview_ids = list(df_video.loc[
                                  (df_video['author'] == author) | (df_video['tag1'].isin(tags)) | (
                                      df_video['tag2'].isin(tags)) | (
                                      df_video['tag3'].isin(tags)), 'video_id'])
    if video_id in video_overview_ids:
        video_overview_ids.remove(video_id)
    cf.print_header()
    with st.container(border=False):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(
                f'''<p style="font-size:36px; text-align:left; font-family:Tahoma;"><strong>''' + name + '''</strong></p>''',
                unsafe_allow_html=True)
    ov.print_tags(video_id)

    with st.container():
        a = st.empty()
        with a:
            st.video(link)
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns(10, gap='large')
        if str(stc) != 'nan':
            with c1:
                if str(stc) != 'nan':
                    if st.button('Début de la conférence'):
                        skip_time = cf.get_sec_from_tc(pd.to_datetime(stc))
                        with a:
                            st.video(link, start_time=skip_time, autoplay=True)
            with c10:
                if str(qtc) != 'nan':
                    if st.button("Passer aux questions"):
                        skip_time = cf.get_sec_from_tc(pd.to_datetime(qtc))
                        with a:
                            st.video(link, start_time=skip_time, autoplay=True)

    with st.container():
        st.header('Conférences connexes')
        st.markdown(' ')
        ov.print_video_overview(video_overview_ids)
