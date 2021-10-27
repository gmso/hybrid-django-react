import os

def add_custom_user_from_docker():
    """Adds custom user to django project"""
    os.system("docker-compose exec web python manage.py startapp users")
    with open("users/models.py", 'w') as f:
        f.write(
            "from django.contrib.auth.models import AbstractUser\n\n"
            "class CustomUser(AbstractUser):"
            "   pass"
        )
