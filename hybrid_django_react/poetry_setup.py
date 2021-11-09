import re
import os


def setup_poetry(config):
    """Entry point of module: setup poetry files and run poetry commands"""
    update_pyproject_dot_toml(config)
    #lock_poetry_dependencies()
    #install_dependencies()


def lock_poetry_dependencies_on_docker():
    """Create poetry.lock file"""
    os.system("docker-compose exec web poetry lock")


def install_dependencies():
    """Install package dependencies"""
    os.system("poetry install")


def update_pyproject_dot_toml(config):
    filename = "pyproject.toml"
    with open(filename) as f:
        content = f.read()
    for p in ("name", "description", "license"):
        content = re.sub(rf'({p}) = ""', f'{p} = "{config[p]}"', content)
    content = re.sub(r'(AUTHOR_POETRY)', config["author"], content)
    content = re.sub(r'(mail@mail.com)', config["email"], content)
    with open(filename, 'w') as f:
        f.write(content)
