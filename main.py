import streamlit as st
from author import print_author_overview, print_rock_star
from tag import print_tag_overview
from ranking import print_ranking_overview
from categories import print_cat_overview
from utils import print_header, print_footer, df_author_overview, df_cat_overview, df_tags_overview

def main():
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    print_header(bar=False)
    count_author = int(len(df_author_overview))
    count_cat = len(df_cat_overview) - 1  # for Interview
    count_tag = len(df_tags_overview)
    t1, t2, t3, t4, t5 = st.tabs(['Rock Stars', f'Thèmes ({count_cat})', f'Tags ({count_tag})', f'Intervenants ({count_author})', 'Meilleures vidéos'])
    with t1:
        print_rock_star()
    with t2:
        print_cat_overview()
    with t3:
        print_tag_overview()
    with t4:
        print_author_overview()
    with t5:
        print_ranking_overview()
    print_footer()
main()
