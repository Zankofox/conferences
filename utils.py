import pandas as pd
import streamlit as st

def print_header(bar=True):
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
    if bar:
        st.markdown('----------------------------------------------------------------------------')


def get_sec_from_tc(tc):
    return tc.hour * 3600 + tc.minute * 60 + tc.second


def get_tag_id_from_name(tag_name):
    df_tags = get_df_tags(df_video)
    dico_tag_name = df_tags[['tag', 'tag_id']].set_index('tag').to_dict(orient='index')
    return dico_tag_name[tag_name]['tag_id']


def get_author_id_from_name(author_name):
    df_author = get_df_author(df_video)
    dico_author_name = df_author[['author', 'author_id']].set_index('author').to_dict(orient='index')
    return dico_author_name[author_name]['author_id']


def get_df_author(df_video):
    df_author = df_video.copy(deep=True)
    df_author_count = df_author['author'].value_counts().reset_index()
    df_author = df_author.merge(df_author_count, on='author', how='left')
    df_author = df_author[['author', 'name', 'link', 'tn_link', 'count']].groupby('author').first().reset_index()
    df_author['author_id'] = [x for x in range(1, len(df_author) + 1)]
    return df_author


def get_df_tags(df_video):
    # CONCAT
    df_tag1 = df_video.loc[~df_video['tag1'].isna(), ['tag1', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag1': 'tag'})
    df_tag2 = df_video.loc[~df_video['tag2'].isna(), ['tag2', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag2': 'tag'})
    df_tag3 = df_video.loc[~df_video['tag3'].isna(), ['tag3', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag3': 'tag'})
    df_tags = pd.concat([df_tag1, df_tag2, df_tag3])

    # FORMATTING
    df_tags['name2'] = df_tags['tag'].str.lower()
    for element in ['le ', 'la ', "l'", 'les ']:
        df_tags['name2'] = df_tags['name2'].str.replace(element, '')

    for element in ['é', 'è', 'ê']:
        df_tags['name2'] = df_tags['name2'].str.replace(element, 'e')

    for element in ['ô', 'ö']:
        df_tags['name2'] = df_tags['name2'].str.replace(element, 'o')

    # ADD COUNT
    df_tag_count = df_tags['tag'].value_counts().reset_index()
    df_tags = df_tags.merge(df_tag_count, on='tag', how='left')
    df_tags = df_tags.groupby('tag').first().reset_index()

    df_tags['tag_id'] = [x for x in range(1, len(df_tags) + 1)]
    df_tags = df_tags.sort_values(by='name2')
    return df_tags


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
    author_id = get_author_id_from_name(author_name)

    elements = []
    if str(tag1) != 'nan':
        tag1_id = get_tag_id_from_name(tag1)
        elements.append(get_tag_md(tag1_id, tag1, 'tag'))
    if str(tag2) != 'nan':
        tag2_id = get_tag_id_from_name(tag2)
        elements.append(get_tag_md(tag2_id, tag2, 'tag'))
    if str(tag3) != 'nan':
        tag3_id = get_tag_id_from_name(tag3)
        elements.append(get_tag_md(tag3_id, tag3, 'tag'))

    if ignore_authors is False:
        if str(author_id) != '':
            author_md = get_tag_md(author_id, author_name, 'author')
        elements.append(author_md)

    sep = f""" """
    final_md = sep.join(elements)
    st.markdown(final_md, unsafe_allow_html=True)

def get_tag_video(df_video):
    df_tag_video = df_video
    return df_tag_video


# VIDEOS
df_video = pd.read_excel('conf.xlsx')
dico_video = df_video.set_index('video_id').to_dict(orient='index')

# AUTHORS
df_author = get_df_author(df_video)
dico_author = df_author.set_index('author_id').to_dict(orient='index')

# TAGS
df_tags = get_df_tags(df_video)
dico_tag = df_tags.set_index('tag_id').to_dict(orient='index')
