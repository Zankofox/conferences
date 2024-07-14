from video import print_video_overview
from utils import df_video
import streamlit as st
import random as rnd
def print_ranking_overview():
    best_rank = 5
    df_video_ranked = df_video.sort_values(by='ranking', ascending=False)
    ranked_ids_temp = list(df_video_ranked.loc[df_video_ranked['ranking'] == best_rank, 'video_id'])
    rnd.shuffle(ranked_ids_temp)
    st.markdown(f"""
            <div style="font-family: Lato; font-size: 24px; padding-bottom: 10px;">
            <span style="font-size: 38px;font-weight: bold;">Ci-dessous sont des bangers</span>
            </div>
            """, unsafe_allow_html=True)
    print_video_overview(ranked_ids_temp)

def print_top50():
    df_video_ranked = df_video.sort_values(by='ranking', ascending=False)
    ranked_ids = list(df_video_ranked['video_id'])
    print_video_overview(ranked_ids)