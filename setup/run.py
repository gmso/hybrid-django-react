import os, sys, subprocess

from user_config import get_user_config
from poetry_setup import setup_poetry
from pytest_setup import setup_pytest
from django_project_setup import create_django_project 


def destroy_setup():
    """Destroy the setup folder with all its content, including this script"""
    subprocess.Popen(
        "python -c \""
        "import shutil, time; "
        "time.sleep(1); "
        f"shutil.rmtree('os.path.dirname({os.path.realpath(__file__)}');\""
    )
    sys.exit(0)


def main():
    """Main entry point"""
    config = get_user_config()
    setup_poetry(config)
    setup_pytest(config)
    create_django_project(config)
    destroy_setup()


if __name__ == "__main__":
    main()