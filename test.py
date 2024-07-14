from utils import df_cat_overview, df_video

cat_name = "Philosophie"
video_ids = list(df_video.loc[(df_video['cat1'] == f'{cat_name}') | (df_video['cat2'] == f'{cat_name}')])
x = 4