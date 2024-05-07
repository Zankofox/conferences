import pandas as pd
import streamlit as st
import numpy as np
import datetime
df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
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
    df_author = df_video[['author', 'name', 'link', 'tn_link']].groupby('author').first().reset_index()
    df_author['author_id'] = [x for x in range(1, len(df_author)+1)]
    return df_author

def get_df_tags(df_video):
    final_tags = list(set(list(df_video['tag1']) + list(df_video['tag2']) + list(df_video['tag3'])))
    df_tag1 = df_video.loc[~df_video['tag1'].isna(), ['tag1', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag1': 'tag'})
    df_tag2 = df_video.loc[~df_video['tag2'].isna(), ['tag2', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag2': 'tag'})
    df_tag3 = df_video.loc[~df_video['tag3'].isna(), ['tag3', 'link', 'tn_link', 'name', 'author']].rename(
        columns={'tag3': 'tag'})
    df_tags = pd.concat([df_tag1, df_tag2, df_tag3])
    df_tags = df_tags.groupby('tag').first().reset_index()
    df_tags['tag_id'] = [x for x in range(1, len(df_tags)+1)]
    return df_tags

