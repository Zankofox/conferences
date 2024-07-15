import streamlit as st
from author import print_author_overview, print_rock_star
from tag import print_tag_overview
from ranking import print_ranking_overview, print_all_ranked
from categories import print_cat_overview
from utils import print_header, print_footer, df_author_overview, df_cat_overview, df_tags_overview

@st.cache_data
def main():
    print_header(bar=False)
    count_author = int(len(df_author_overview))
    count_cat = len(df_cat_overview) - 1  # for Interview
    count_tag = len(df_tags_overview)
    t1, t2, t3, t4, t5 = st.tabs(['Meilleures vidéos', 'Rock Stars', f'Thèmes ({count_cat})', f'Intervenants ({count_author})', f'Tags ({count_tag})'])
    with t1:
        print_ranking_overview()
    with t2:
        print_rock_star()
    with t3:
        print_cat_overview()
    with t4:
        print_author_overview()
    with t5:
        print_tag_overview()

    print_footer()
st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
main()
