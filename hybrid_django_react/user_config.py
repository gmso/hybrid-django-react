def get_user_config():
    """Entry point: Get user configuration"""
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

def get_user_input(prompt:str, default:str):
    """Get user input"""
    user_input = input(f"{prompt} [{default}]: ")
    if not user_input:
        user_input = default
    return user_input
