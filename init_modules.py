import os
import utils as ut

df_video = ut.df_video
dico_video = ut.dico_video
df_author = ut.df_author
df_tags = ut.df_tags
dico_tags = ut.dico_tag

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

def file_exists_in_current_directory(file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory+ '\\pages', file_name)
    return os.path.exists(file_path)

def create_module_author(author_id):
    code = f"""from author import page_author
page_author({author_id})"""
    create_module("./pages", f'author_{author_id}', code=code)

def check_upload_author(df_author):
    for author_id in list(df_author['author_id']):
        module_name= f'author_{author_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_author(author_id)



def create_module_tag(tag_id):
    code = f"""from tag import page_tag
page_tag({tag_id})"""
    create_module("./pages", f'tag_{tag_id}', code=code)

def check_upload_tags(df_tags):
    for tag_id in list(df_tags['tag_id']):
        module_name= f'tag_{tag_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_tag(tag_id)

def create_module_video(video_id):
    code = f"""from video import page_video
page_video({video_id})"""
    create_module("./pages", f'video_{video_id}', code=code)

def check_upload_video(df_video):
    for video_id in list(df_video['video_id']):
        module_name = f'video_{video_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_video(video_id)


def check_upload_all():
    check_upload_video(df_video)
    check_upload_tags(df_tags)
    check_upload_author(df_author)

check_upload_all()