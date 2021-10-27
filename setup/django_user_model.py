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
    str_to_find = '#AUTH_USER_MODEL'
    new_str = 'AUTH_USER_MODEL'
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            if str_to_find in line:
                new_line = line.replace(str_to_find, new_str)
                f_new.write(new_line+"\n")
            else:
                f_new.write(line)
