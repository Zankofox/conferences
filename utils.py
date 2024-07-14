import streamlit as st
import pandas as pd
from datetime import datetime
import os
import shutil
import config as cf
import base64

def move_and_rename_file_if_exists(file_path, target_directory, new_file_name):
    # Debugging: Print input parameters
    print(f"file_path: {file_path}")
    print(f"target_directory: {target_directory}")
    print(f"new_file_name: {new_file_name}")

    # Check for invalid characters in new_file_name
    invalid_chars = '<>:"/\\|?*'
    if any(char in new_file_name for char in invalid_chars):
        print(f"Error: The new file name '{new_file_name}' contains invalid characters.")
        return

    # Ensure the file exists
    if os.path.exists(file_path):
        # Ensure the target directory exists
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Construct the new file path
        new_file_path = os.path.join(target_directory, new_file_name)

        # Debugging: Print new file path
        print(f"new_file_path: {new_file_path}")

        # Move and rename the file
        try:
            shutil.move(file_path, new_file_path)
            print(f"File '{file_path}' moved to '{new_file_path}' successfully.")
        except Exception as e:
            print(f"Error moving file '{file_path}': {e}")
    else:
        print(f"File '{file_path}' does not exist.")


def check_and_delete_file(filepath):
    """Check if a file exists and delete it if it does."""
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"File '{filepath}' has been deleted.")
        else:
            print(f"File '{filepath}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def print_header(bar=True):
    count_video = len(df_video)
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>""", unsafe_allow_html=True)

    st.markdown(f'''<div style="text-align: center;">
    <a style="font-size: 52px; font-family: Tahoma; text-decoration: none; color: #ffffff;" href='/main' target="_self"><strong>Conférences.fr 💡</strong></a>
</div>''', unsafe_allow_html=True)

    st.markdown(f"""
            <div style="font-family: Lato; text-align: center; font-size: 14px;">
            <span style="font-size: 14px; "><em>{count_video} conférences disponibles </em></span>
            </div>
            """, unsafe_allow_html=True)
    if bar:
        st.markdown('----------------------------------------------------------------------------')


def print_footer():
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(f"""
            <div style="font-family: Lato; text-align: right; font-size: 24px; padding-bottom: 10px;">
            <span style="font-size: 14px; "><em>Version {cf.VERSION}</em></span>
            </div>
            """, unsafe_allow_html=True)


def get_sec_from_tc(tc):
    return tc.hour * 3600 + tc.minute * 60 + tc.second


# def get_tag_id_from_name(tag_name):
#
#     dico_tag_name = df_tags_full[['tag', 'tag_id']].set_index('tag').T.to_dict(orient='index')
#     return dico_tag_name['tag_id'][tag_name]


def get_author_id_from_name(author_name):
    return dico_author_name[author_name]['author_id']

def get_cat_id_from_name(cat_name):
    return dico_cat_name[cat_name]['cat_id']


# def get_df_author(df_video):
#     df_author = df_video.copy(deep=True)
#     df_author_count = df_author['author'].value_counts().reset_index()
#     df_author = df_author.merge(df_author_count, on='author', how='left')
#     df_author = df_author[['author', 'name', 'link', 'tn_link', 'count']].groupby('author').first().reset_index()
#     df_author['author_id'] = [x for x in range(1, len(df_author) + 1)]
#     return df_author


def get_tag_md(tag_id, name, type='tag'):
    if type == 'author':
        bg_color = '#da7653'
    else:
        bg_color = '#293961'
    final_md = f"""<a style='font-family: Lato; font-size: 14px; font-weight: bold;text-decoration:none;color:#ffffff;background-color:{bg_color};padding:4px 8px;border-radius:3px;' href='/{type}_{tag_id}'><em>{name}</em></a> &nbsp;&nbsp;&nbsp;"""
    return final_md


def print_tags(video_id, height, ignore_author=False):
    video_name = df_video.loc[df_video['video_id'] == video_id, 'name'].values[0]
    dico_tags = df_tags.loc[df_tags['name'] == video_name, ['tag', 'tag_id']].set_index('tag_id').to_dict(
        orient='index')
    author_name = dico_video[video_id]['author']
    author_id = get_author_id_from_name(author_name)

    elements = []
    for k, v in dico_tags.items():
        if str(v['tag']) != 'nan':
            tag_md = get_tag_md(k, v['tag'], 'tag')
            elements.append(tag_md)
    if ignore_author is False:
        if str(author_id) != '':
            author_md = get_tag_md(author_id, author_name, 'author')
        elements.append(author_md)

    sep = f""" """
    final_md = sep.join(elements)

    a = st.container(border=False, height=height)
    with a:
        st.markdown(final_md, unsafe_allow_html=True)

def get_max_len(video_ids):
    max_len = 0
    for video_id in video_ids:
        video_name = df_video.loc[df_video['video_id'] == video_id, 'name'].values[0]
        dico_tags = df_tags.loc[df_tags['name'] == video_name, ['tag', 'tag_id']].set_index('tag_id').to_dict(
            orient='index')
        author_name = dico_video[video_id]['author']
        tags_string = ''
        for k, v in dico_tags.items():
            if str(v['tag']) != 'nan':
                tags_string = tags_string + '  ' + v['tag']
        final_string = tags_string + ' ' + author_name
        if len(final_string) > max_len:
            max_len = len(final_string)
    return max_len


def transform_date(date):
    # Get delta from today
    delta_int = (datetime.today() - date).days
    if delta_int < 30:
        final_string = f"il y a {delta_int} jours"

    elif (delta_int >= 30) & (delta_int < 365):
        final_string = f"il y a {int(delta_int / 30)} mois"

    elif (delta_int) >= 365 & (delta_int < 5 * 365):
        final_string = f"il y a {int(delta_int / 365)} ans"

    else:
        final_string = f"il y a + de 5 ans"

    return final_string

def get_video(df_video):
    # Add publish date
    df_video['delta_date_int'] = [(datetime.today() - x).days for x in list(df_video['publish_date'])]
    df_video['delta_date_string'] = [transform_date(x) for x in list(df_video['publish_date'])]
    return df_video

def get_df_author(df_video):
    df_author = df_video.copy(deep=True)
    df_author_count = df_author['author'].value_counts().reset_index()
    df_author_count['author_id'] = [x for x in range(1, len(df_author_count) + 1)]
    df_author = df_author.merge(df_author_count, on='author', how='left')
    return df_author


def get_df_author_overview(df_author):
    df_author_overview = df_author.groupby('author_id').first().reset_index()
    return df_author_overview


def get_df_tags(df_video):
    df_tags = pd.DataFrame()
    for i in range(1, cf.MAX_TAGS):
        df_to_add = df_video.loc[~df_video[f'tag{i}'].isna(), [f'tag{i}', 'link', 'tn_link', 'name', 'author']].rename(
            columns={f'tag{i}': 'tag'})
        df_tags = pd.concat([df_tags, df_to_add])

    # ADD COUNT
    df_tags_id = df_tags[['tag', 'name']].groupby('tag').first().reset_index()
    df_tags_id['tag_id'] = [x for x in range(1, len(df_tags_id) + 1)]
    df_tags_count = df_tags['tag'].value_counts().reset_index()
    df_tags_count_id = df_tags_count[['tag', 'count']].merge(df_tags_id[['tag', 'tag_id']], on='tag', how='left')
    df_tags = df_tags.merge(df_tags_count_id, on='tag', how='left')
    df_tags = df_tags.sort_values(by='tag_id')
    return df_tags


def get_df_tags_overview(df_tags):
    df_tags_overview = df_tags.groupby('tag').first().reset_index()
    return df_tags_overview

def get_df_cats(df_rockstar):
    df_cats = pd.DataFrame()
    for i in range(1, cf.MAX_CATS):
        df_to_add = df_video.loc[
            ~df_video[f'cat{i}'].isna(), [f'cat{i}', 'link', 'tn_link', 'name', 'author']].rename(
            columns={f'cat{i}': 'cat'})
        df_cats = pd.concat([df_cats, df_to_add])

    # ADD COUNT
    df_cats_id = df_cats[['cat', 'name']].groupby('cat').first().reset_index()
    df_cats_id['cat_id'] = [x for x in range(1, len(df_cats_id) + 1)]
    df_cats_count = df_cats['cat'].value_counts().reset_index()
    df_cats_count_id = df_cats_count[['cat', 'count']].merge(df_cats_id[['cat', 'cat_id']], on='cat', how='left')
    df_cats = df_cats.merge(df_cats_count_id, on='cat', how='left')
    df_cats = df_cats.sort_values(by='cat_id')
    return df_cats

def get_df_cats_overview(df_cats):
    df_cats_overview = df_cats.groupby('cat').first().reset_index()
    return df_cats_overview

def get_quote_size(quote):
    start_font = 26
    quote_size = int(max(start_font - (len(quote) / 80), 18))
    return quote_size

def display_menu(link_page, image_path, cat_name, count_video):
    def get_image_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    image_base64 = get_image_base64(image_path)
    html_code = f"""<div style="display: flex; justify-content: center; align-items: center; height: 50;">
<a href="{link_page}" target="_blank">
    <img src="data:image/png;base64,{image_base64}" style="width:350px; height:350px; padding-top:5px; padding-bottom:10px;">
</a>
</div>"""
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown(f"""
            <div style="font-family: Lato; font-size: 32px; padding-bottom: 10px; text-align: center;">
            <span style="font-weight: bold;">{cat_name}</span>
            <span style="font-size: 20px;">({count_video})</span>
            </div>
            """, unsafe_allow_html=True)


def display_photo(link_page, image_path, width=1100, height=500):
    def get_image_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    image_base64 = get_image_base64(image_path)
    html_code = f'''
    <a href="{link_page}" target="_blank">
        <img src="data:image/png;base64,{image_base64}" style="width:{width}px;height:{height};padding-top:5px;padding-bottom:10px;">
    </a>
    '''
    st.markdown(html_code, unsafe_allow_html=True)


df_input = pd.read_excel('input.xlsx')
df_rockstar = pd.read_excel('rockstars.xlsx')
df_video = get_video(df_input)
dico_video = df_video.set_index('video_id').to_dict(orient='index')
df_author = get_df_author(df_video)
df_author_overview = get_df_author_overview(df_author)
dico_author = df_author_overview.set_index('author_id').to_dict(orient='index')
dico_author_name = df_author_overview.set_index('author').to_dict(orient='index')
df_tags = get_df_tags(df_video).drop_duplicates()
df_tags_overview = get_df_tags_overview(df_tags)

df_cats = get_df_cats(df_rockstar)
df_cat_overview = get_df_cats_overview(df_cats)
dico_cat = df_cat_overview.set_index('cat_id').to_dict(orient='index')
dico_cat_name = df_cat_overview.set_index('cat').to_dict(orient='index')
dico_tag = df_tags_overview.set_index('tag_id').to_dict(orient='index')


df_quotes = pd.read_excel('quotes.xlsx')
