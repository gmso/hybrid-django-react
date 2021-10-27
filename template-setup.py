import re
import os

def get_user_input(prompt:str, default:str):
    """Get user input"""
    user_input = input(f"{prompt} [{default}]: ")
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
    config["author"] = get_user_input(
        "Author's name", "author"
    )
    config["email"] = get_user_input(
        "Author's email", "author@mail.com"
    )
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
    for p in ("name", "description", "license"):
        content = re.sub(rf'({p}) = ""', f'{p} = "{config[p]}"', content)
    content = re.sub(r'(AUTHOR_POETRY)', config["author"], content)
    content = re.sub(r'(mail@mail.com)', config["email"], content)
    with open(filename, 'w') as f:
        f.write(content)


def update_pytest_dot_ini(config):
    filename = "pytest.ini"
    with open(filename) as f:
        content = f.read()
    content = re.sub(r'(PROJECT)', f'{config["name"]}', content)
    with open(filename, 'w') as f:
        f.write(content)


def update_manage_dot_py(config):
    """Adds VSCode debugging support to manage.py"""
    filename = "manage.py"
    temp_name = f"{filename}_new.txt"
    new_content = ("""\
    from django.conf import settings
    if settings.DEBUG:
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import ptvsd

            ptvsd.enable_attach(address=("0.0.0.0", 5678))
            # ptvsd.wait_for_attach()
            print("Attached!")"""
    )
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            if 'try:' in line:
                f_new.write(new_content+"\n")
            f_new.write(line)
    os.remove(filename)
    os.rename(temp_name,filename)


def main():
    """Main entry point"""
    config = get_user_configuration()
    update_pyproject_dot_toml(config)
    update_pytest_dot_ini(config)
    create_django_project(config["name"])
    update_manage_dot_py(config)


if __name__ == "__main__":
    main()