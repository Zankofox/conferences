import streamlit as st
from author import print_author_overview
from tag import print_tag_overview
import utils as ut

def main():
    st.set_page_config(page_title='Conférences.fr', page_icon='💡', layout='wide')
    ut.print_header(bar=False)
    t1, t2 = st.tabs(['Intervenants', 'Thèmes'])
    with t1:
        print_author_overview()
    with t2:
        print_tag_overview()
main()
