import os, sys, subprocess

from .user_config import get_user_config
from .poetry_setup import setup_poetry, lock_poetry_dependencies_on_docker
from .pytest_setup import setup_pytest
from .django_project_setup import create_django_project
from .docker_build import docker_build_and_start, docker_stop
from .django_user_model import add_custom_user_from_docker
from .urls_setup import change_project_urls
from .format_code import format_with_black
from .copy_assets import copy_assets_to_current_dir


def destroy_setup():
    """Destroy the setup folder with all its content, including this script"""
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path).replace("\\","\\\\")
    subprocess.Popen(
        "python -c \""
        "import shutil, time; "
        "time.sleep(1); "
        f"shutil.rmtree('{dir_path}');\"",
        shell=True,
    )
    sys.exit(0)


def greet():
    """Greet user and output information"""
    print("\n\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print("■■■  Hybrid Django React Starter Project  ■■")
    print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print("\n\n■■ Setting up project structure ■■\n")


def main():
    """Main entry point"""
    greet()
    print("\n  ■ Please introduce the project's metadata\n")
    config = get_user_config()
    
    print("\n  ■ Copying assets\n")
    copy_assets_to_current_dir()

    print("\n  ■ Customizing poetry files\n")
    setup_poetry(config)
    
    print("\n  ■ Customizing pytest files\n")
    setup_pytest(config)

    print("\n  ■ Creating Django project\n")
    create_django_project(config)
    
    print("\n  ■ Initializing Docker container\n")
    docker_build_and_start()

    #print("\n  ■ Locking poetry dependencies\n")
    #lock_poetry_dependencies_on_docker()

    print("\n  ■ Creating custom User in Django app 'users'\n")
    add_custom_user_from_docker(config)

    print("\n  ■ Changing urls of project\n")
    change_project_urls(config)

    print("\n  ■ Formatting python files\n")
    format_with_black()

    print("\n  ■ Stopping Docker container\n")
    docker_stop()
    
    print("\n  ■ Finishing...\n")
    # destroy_setup()

    print("\n\n■■ Finished! Your Django React project is set up! ■■\n")

    print("\n\n■ To start working, spin up your container with the command 'docker-compose up -d'\n")

    print("\n\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print("■■■  Thank you for using this Hybrid Django React Starter Project, bye!  ■■")
    print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■\n\n")

if __name__ == "__main__":
    main()