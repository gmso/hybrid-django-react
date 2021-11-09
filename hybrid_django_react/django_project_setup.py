import os
import shutil
import sys

from .django_settings_content_changes import get_settings_dot_py_changes


def create_django_project(config):
    """Entry point: Creates django project"""
    #was_in_virtualenv = start_venv_if_needed()
    install_django(config)
    start_project_django_admin(config)
    update_manage_dot_py(config)
    update_settings_dot_py(config)
    
    #if not was_in_virtualenv:
    #    deactivate_and_delete_venv()


def start_venv_if_needed():
    """Start virtual env. if needed. Returns True if it was activated"""
    if not in_virtualenv():
        create_and_activate_venv()
        return False
    return True


def install_django(config):
    """Install Django with pip"""
    os.system("pip install Django==3.2.6")

def start_project_django_admin(config):
    #os.system(f"docker-compose exec web django-admin startproject {config['name']} .")
    os.system(f"django-admin startproject {config['name']} .")

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


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix


def is_os_windows():
    return os.name == "nt"


def create_and_activate_venv():
    os.system("python -m venv .tempvenv")
    if is_os_windows():
        os.system(".tempvenv/scripts/activate")
    else:
        os.system(".tempvenv/bin/activate")

def deactivate_and_delete_venv():
    os.system("deactivate")
    shutil.rmtree(".tempvenv")