import os


def add_custom_user_from_docker(config):
    """Adds custom user to django project"""

    # Create Django app
    os.system("docker-compose exec web python manage.py startapp users")

    # Modify users/models.py to use AbstractUser
    with open("users/models.py", 'w') as f:
        f.write(
            "from django.contrib.auth.models import AbstractUser\n\n"
            "class CustomUser(AbstractUser):\n"
            "   pass"
        )

    # Point to custom user in settings.py
    filename = f"{config['name']}/settings.py"
    temp_name = f"{filename}_new.txt"
    old_strings = (
        '# Local\n',
        '#AUTH_USER_MODEL',
    )
    new_strings = (
        '# Local\n    "users.apps.UsersConfig",\n',
        'AUTH_USER_MODEL',
    )
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            for i, old in enumerate(old_strings):
                if old in line:
                    new_line = line.replace(old, new_strings[i])
                    f_new.write(new_line+"\n")
                    break
            else:
                f_new.write(line)
    os.remove(filename)
    os.rename(temp_name,filename)

    # Perform database migration
    os.system("docker-compose exec web python manage.py makemigrations")
    os.system("docker-compose exec web python manage.py migrate")
