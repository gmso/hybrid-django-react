from user_config import get_user_config
from poetry_setup import setup_poetry
from pytest_setup import setup_pytest
from django_project_setup import create_django_project 


def main():
    """Main entry point"""
    config = get_user_config()
    setup_poetry(config)
    setup_pytest(config)
    create_django_project(config)


if __name__ == "__main__":
    main()