import re
import os

def get_user_input(prompt:str, default:str):
    """Get user input"""
    user_input = input(f"{prompt} [{default}]")
    if not user_input:
        user_input = default
    return user_input


def get_user_configuration():
    """Get user configuration"""
    config = {}
    config["name"] = get_user_input(
        "Django project name", "django_project"
    )
    config["description"] = get_user_input(
        "Django project description", "Awesome project"
    )
    author = get_user_input("Author's name", "author")
    email = get_user_input("Author's email", "author@mail.com")
    config["authors"] = f"[{author} <{email}>]"
    config["license"] = get_user_input(
        "Software license", "MIT License"
    )
    return config


def create_django_project(name: str):
    """Creates django project"""
    os.system("poetry install")
    os.system(f"poetry run django-admin startproject {name} .")


def update_pyproject_dot_toml(config):
    filename = "pyproject.toml"
    with open(filename) as f:
        content = f.read()
    for p in ("name", "description", "authors", "license"):
        content = re.sub(f'{f} = ""', f'{f} = "{config[p]}"', content)
    with open(filename, 'w') as f:
        f.write(content)


def update_pytest_dot_ini(config):
    filename = "pytest.ini"
    with open(filename) as f:
        content = f.read()
    content = re.sub('PROJECT', f'{f} = "{config["name"]}"', content)
    with open(filename, 'w') as f:
        f.write(content)



def main():
    """Main entry point"""
    config = get_user_configuration()
    update_pyproject_dot_toml(config)
    update_pytest_dot_ini(config)
    create_django_project(config["name"])


if __name__ == "__main__":
    main()