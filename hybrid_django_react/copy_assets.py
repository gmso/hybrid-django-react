import os
from distutils.dir_util import copy_tree


def copy_assets_to_current_dir():
    file_path = os.path.realpath(__file__)
    assets_path = os.path.join(file_path, "../assets")
    files = os.listdir(assets_path)

    current_directory_path = os.getcwd()

    copy_tree(assets_path, current_directory_path)
