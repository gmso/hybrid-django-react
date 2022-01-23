import os
from distutils.dir_util import copy_tree
from pathlib import Path

def copy_assets_to_current_dir():
    file_path = Path(__file__).resolve().parent
    assets_path = f'{file_path}/assets'
    files = os.listdir(assets_path)
    current_directory_path = os.getcwd()
    copy_tree(assets_path, current_directory_path)
