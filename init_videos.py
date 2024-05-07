import pandas as pd
import os

df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
dico_video = df_video.set_index('video_id').to_dict(orient='index')


def create_module(folder_path, module_name, code):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    module_path = os.path.join(folder_path, f"{module_name}.py")
    if os.path.exists(module_path):
        print(f"Module '{module_name}' already exists in '{folder_path}'. Skipping creation.")
        return

    # Write the code to the module file
    with open(module_path, "w") as file:
        file.write(code)
    print(f"Module '{module_name}' created in '{folder_path}'")


def create_module_video(video_id):
    link = dico_video[video_id]['link']
    code = f"""from video import page_video
page_video({video_id})"""
    create_module("./pages", f'video_{video_id}', code=code)


def file_exists_in_current_directory(file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory + '\\pages', file_name)
    return os.path.exists(file_path)

def check_upload_video(df_video):
    for video_id in list(df_video['video_id']):
        module_name = f'video_{video_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_video(video_id)


check_upload_video(df_video)
