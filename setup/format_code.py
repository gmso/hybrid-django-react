import os


def format_with_black():
    """Format python files with black"""
    os.system("docker-compose exec web black .")
