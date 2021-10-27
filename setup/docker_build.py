import os


def docker_build_and_start():
    """Build docker image and start docker container"""
    os.system("docker-compose up -d --build")


def docker_stop():
    """Stop docker container"""
    os.system("docker-compose down")
