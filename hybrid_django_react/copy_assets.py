import os
import shutil


def copy_assets_to_current_dir():
    file_path = os.path.realpath(__file__)
    assets_path = os.path.join(file_path, "assets")
    files = os.listdir(assets_path)

    current_directory_path = os.getcwd()

    shutil.copytree(assets_path, current_directory_path)
