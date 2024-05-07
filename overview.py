import streamlit as st
import pandas as pd
import conf_utils as cf

df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
dico_video = df_video.set_index('video_id').to_dict(orient='index')
df_author = cf.get_df_author(df_video)
dico_author = df_author.set_index('author_id').to_dict(orient='index')
df_tags = cf.get_df_tags(df_video)
dico_tag = df_tags.set_index('tag_id').to_dict(orient='index')

def print_tag_overview(df_tags):
    st.title('Thèmes')
    dico_tag = df_tags.set_index('tag_id').to_dict(orient='index')
    nb_cols = 4
    image_width_percent = 100
    c1, c2, c3, c4 = st.columns(nb_cols)
    counter = 0
    for tag_id in list(df_tags['tag_id']):
        link_page = f'/tag_{tag_id}'
        image_url = dico_tag[tag_id]['tn_link']
        tag_name = dico_tag[tag_id]['tag']
        markdown_string = f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{image_width_percent}%;height:auto;"></a>'
        def print_temp():
            a = st.container(border=True)
            with a:
                st.markdown(markdown_string, unsafe_allow_html=True)
                st.markdown(
                    f'<p style="font-family: Lato; font-size: 24px; font-weight: bold;">{tag_name}</p>',
                    unsafe_allow_html=True)
        if counter % nb_cols == 0:
            with c1:
                print_temp()
        if counter % nb_cols == 1:
            with c2:
                print_temp()
        if counter % nb_cols == 2:
            with c3:
                print_temp()
        if counter % nb_cols == 3:
            with c4:
                print_temp()

        counter += 1
def print_author_overview(df_author):
    st.title('Intervenants')
    dico_author = df_author.set_index('author_id').to_dict(orient='index')
    nb_cols = 3
    image_width_percent = 100
    c1, c2, c3 = st.columns(nb_cols)
    counter = 0
    for author_id in list(df_author['author_id']):
        link_page = f'/author_{author_id}'
        image_url = dico_author[author_id]['tn_link']
        author_name = dico_author[author_id]['author']
        markdown_string = f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{image_width_percent}%;height:auto;"></a>'
        def print_temp():
            a = st.container(border=True)
            with a:
                st.markdown(markdown_string, unsafe_allow_html=True)
                st.markdown(
                    f'<p style="font-family: Lato; font-size: 24px; font-weight: bold;">{author_name}</p>',
                    unsafe_allow_html=True)
        if counter % nb_cols == 0:
            with c1:
                print_temp()
        if counter % nb_cols == 1:
            with c2:
                print_temp()
        if counter % nb_cols == 2:
            with c3:
                print_temp()
        counter += 1

def print_video_info(video_id):
    dico_temp = dico_video[video_id]
    st.markdown('')

def print_tags(video_id, ignore_authors=False):
    def get_tag_md(id, name, type='tag'):
        if type == 'author':
            bg_color = '#da7653'
        else:
            bg_color = '#293961'
        return f"""<a style='font-family: Lato; font-size: 14px; font-weight: bold;text-decoration:none;color:#ffffff;background-color:{bg_color};padding:4px 8px;border-radius:3px;' href='/{type}_{id}'><em>{name}</em></a> &nbsp;&nbsp;&nbsp;"""

    tag1 = dico_video[video_id]['tag1']
    tag2 = dico_video[video_id]['tag2']
    tag3 = dico_video[video_id]['tag3']
    author_name = dico_video[video_id]['author']
    author_id = cf.get_author_id_from_name(author_name)

    elements = []
    if str(tag1) != 'nan':
        tag1_id = cf.get_tag_id_from_name(tag1)
        elements.append(get_tag_md(tag1_id, tag1, 'tag'))
    if str(tag2) != 'nan':
        tag2_id = cf.get_tag_id_from_name(tag2)
        elements.append(get_tag_md(tag2_id, tag2, 'tag'))
    if str(tag3) != 'nan':
        tag3_id = cf.get_tag_id_from_name(tag3)
        elements.append(get_tag_md(tag3_id, tag3, 'tag'))

    if ignore_authors is False:
        if str(author_id) != '':
            author_md = get_tag_md(author_id, author_name, 'author')
        elements.append(author_md)

    sep = f""" """
    final_md = sep.join(elements)
    st.markdown(final_md, unsafe_allow_html=True)

def print_video_overview(video_ids, ignore_author=False):
    nb_cols = 3
    image_width_percent = 100
    c1, c2, c3 = st.columns(nb_cols)
    counter = 0
    for video_id in video_ids:
        dico_video_temp = dico_video[video_id]
        link_page = f'/video_{video_id}'
        link_youtube = dico_video_temp['link']
        image_url = dico_video_temp['tn_link']
        video_name = dico_video_temp['name']
        video_short_name = video_name[:45] + '...'
        if len(video_name) < 48:
            video_short_name = video_name

        author_name = dico_video_temp['author']
        author_id = cf.get_author_id_from_name(author_name)

        video_picture_md = f'<a href="{link_page}" target="_self"><img src="{image_url}" style="width:{image_width_percent}%;height:auto;"></a>'
        video_title_md = f'<p style="font-family: Tahoma; font-size: 20px; font-weight: bold;" title="{video_name}">{video_short_name}</p>'
        def print_top():
            st.markdown(video_title_md, unsafe_allow_html=True)
            st.markdown(video_picture_md, unsafe_allow_html=True)

        if counter % nb_cols == 0:
            with c1:
                a = st.container(border=True)
                with a:
                    print_top()
                    print_tags(video_id, ignore_authors=ignore_author)
        if counter % nb_cols == 1:
            with c2:
                a = st.container(border=True)
                with a:
                    print_top()
                    print_tags(video_id, ignore_authors=ignore_author)
        if counter % nb_cols == 2:
            with c3:
                a = st.container(border=True)
                with a:
                    print_top()
                    print_tags(video_id, ignore_authors=ignore_author)
        counter += 1