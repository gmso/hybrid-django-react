import os

from .django_settings_content_changes import get_settings_dot_py_changes


def create_django_project(config):
    """Entry point: Creates django project"""
    os.system(f"docker-compose exec web django-admin startproject {config['name']} .")
    update_manage_dot_py(config)
    update_settings_dot_py(config)


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


def update_settings_dot_py(config):
    """Updates django's settings.py to template standard"""
    filename = f"{config['name']}/settings.py"
    temp_name = f"{filename}_new.txt"
    
    (INSERTED, SUBSTITUTED, APPENDED) = get_settings_dot_py_changes(config)

    # Add new content
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            for (key, value) in INSERTED.items():
                if key in line:
                    f_new.write(value)
                    INSERTED.pop(key, None)
                    break
            f_new.write(line)
    os.remove(filename)
    os.rename(temp_name,filename)

    # Replace content
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            for (key, value) in SUBSTITUTED.items():
                if key in line:
                    f_new.write(value)
                    SUBSTITUTED.pop(key, None)
                    break
            else:
                f_new.write(line)
    os.remove(filename)
    os.rename(temp_name,filename)

    # Append content
    with open(filename, 'a') as f:
        f.write(APPENDED)
