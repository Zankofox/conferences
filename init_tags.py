import pandas as pd
import os
import conf_utils as cf

df_video = pd.read_excel('conf.xlsx', sheet_name='videos')
df_tags = cf.get_df_tags(df_video)
dico_tags = df_tags.set_index('tag_id').to_dict(orient='index')

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


def create_module_tag(tag_id):
    code = f"""from tag import page_tag
page_tag({tag_id})"""
    create_module("./pages", f'tag_{tag_id}', code=code)
def file_exists_in_current_directory(file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory+ '\\pages', file_name)
    return os.path.exists(file_path)


def check_upload_tags(df_tags):
    for tag_id in list(df_tags['tag_id']):
        module_name= f'tag_{tag_id}.py'
        if file_exists_in_current_directory(module_name):
            print(f"Module '{module_name}' already exists. Skipping creation.")
        else:
            create_module_tag(tag_id)

check_upload_tags(df_tags)