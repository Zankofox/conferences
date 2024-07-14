import os
import utils



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

def check_upload_author(author_ids):
    for author_id in author_ids:
        module_name= f'author_{author_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_author(author_id)



def create_module_tag(tag_id):
    code = f"""from tag import page_tag
page_tag({tag_id})"""
    create_module("./pages", f'tag_{tag_id}', code=code)

def check_upload_tags(tag_ids):
    for tag_id in tag_ids:
        module_name= f'tag_{tag_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_tag(tag_id)

def create_module_cat(cat_id):
    code = f"""from categories import page_cat
page_cat({cat_id})"""
    create_module("./pages", f'cat_{cat_id}', code=code)

def check_upload_cats(cat_ids):
    for cat_id in cat_ids:
        module_name= f'cat_{cat_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_cat(cat_id)

def create_module_video(video_id):
    code = f"""from video import page_video
page_video({video_id})"""
    create_module("./pages", f'video_{video_id}', code=code)

def check_upload_video(video_ids):
    for video_id in video_ids:
        module_name = f'video_{video_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_video(video_id)


def check_upload_all():
    video_ids = list(set(utils.df_video['video_id']))
    author_ids = list(set(utils.df_author['author_id']))
    tag_ids = list(set(utils.df_tags['tag_id']))
    cat_ids = list(set(utils.df_cats['cat_id']))
    check_upload_video(video_ids)
    check_upload_tags(tag_ids)
    check_upload_author(author_ids)
    check_upload_cats(cat_ids)

check_upload_all()