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


def update_settings_dot_py(config):
    """Updates django's settings.py to template standard"""
    filename = f"{config['name']}/settings.py"
    temp_name = f"{filename}_new.txt"
    inserted_content = { # Value inserted before line with key
        "from pathlib import Path": "import sys, os",
        "ALLOWED_HOSTS = []": (
            'if ENVIRONMENT == "production":\n'
            '    SECURE_BROWSER_XSS_FILTER = True\n'
            '    X_FRAME_OPTIONS = "DENY"\n'
            '    SECURE_SSL_REDIRECT = True\n'
            '    SECURE_HSTS_SECONDS = 3600\n'
            '    SECURE_HSTS_INCLUDE_SUBDOMAINS = True\n'
            '    SECURE_HSTS_PRELOAD = True\n'
            '    SECURE_CONTENT_TYPE_NOSNIFF = True\n'
            '    SESSION_COOKIE_SECURE = True\n'
            '    CSRF_COOKIE_SECURE = True\n'
            '    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")\n'
        ),
        "django.contrib.staticfiles": '"whitenoise.runserver_nostatic",\n',
        "# Static files (CSS, JavaScript, Images)": (
            "LOCALE_PATHS = [\n"
            "    os.path.join(BASE_DIR, 'locale'),\n"
            "]\n"
            "LANGUAGES = [\n"
            "   ('en-us', 'English'),\n"
            "   ('es', 'Spanish'),\n"
            "]\n"
        ),
        "STATIC_URL = '/static/'": (
            'STATICFILES_DIRS = [\n'
            '    str(Path(BASE_DIR, "static")),\n'
            ']\n'
            'STATIC_ROOT = str(Path(BASE_DIR, "staticfiles"))\n'
            'STATICFILES_FINDERS = [\n'
            '    "django.contrib.staticfiles.finders.FileSystemFinder",\n'
            '    "django.contrib.staticfiles.finders.AppDirectoriesFinder",\n'
            ']\n'
        ),
    }
    substituted_content = { # Line with key is substituted with content
        "SECRET_KEY = ": 'SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY",default="django-insecure-@04%uk08cz)mpenm#15f*5zg!0(pnc&p@2pzq6shfwi*%h900f",)',
        "DEBUG = True": 'DEBUG = os.environ.get("DJANGO_DEBUG", default="True") == "True"',
        "ALLOWED_HOSTS = []" : 'ALLOWED_HOSTS = ["localhost","127.0.0.1",]',
        '"django.contrib.staticfiles",':(
            '   "django.contrib.staticfiles",\n'
            '   "django.contrib.sites",\n'
            '   # Third party\n'
            '   "allauth",\n'
            '   "allauth.account",\n'
            '   # Local\n'
        ),
        "'django.contrib.sessions.middleware.SessionMiddleware',": (
            "   'whitenoise.middleware.WhiteNoiseMiddleware',\n"
            "   'django.contrib.sessions.middleware.SessionMiddleware',\n"
            "   'django.middleware.locale.LocaleMiddleware',\n"
        ),
        "'ENGINE': 'django.db.backends.sqlite3',": "",
        "'NAME': BASE_DIR / 'db.sqlite3',": (
            '       "ENGINE": "django.db.backends.postgresql",\n'
            '       "NAME": "postgres",\n'
            '       "USER": "postgres",\n'
            '       "PASSWORD": "postgres",\n'
            '       "HOST": "db",\n'
            '       "PORT": 5432,\n'
        ),
    }
    appended_content = ( # Content appended to end of file
        '# Custom User model\n'
        'AUTH_USER_MODEL = "users.CustomUser"\n\n'
        '# django-allauth config\n'
        'LOGIN_REDIRECT_URL = "app:dashboard"\n'
        'ACCOUNT_LOGOUT_REDIRECT = "pages:home"\n\n'
        'SITE_ID = 1\n\n'
        'ACCOUNT_AUTHENTICATION_METHOD = "email"\n'
        'ACCOUNT_EMAIL_REQUIRED = True\n'
        'ACCOUNT_EMAIL_VERIFICATION = "mandatory"\n'
        'ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True\n'
        'ACCOUNT_SESSION_REMEMBER = True\n'
        'ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False\n'
        'ACCOUNT_USERNAME_REQUIRED = False\n'
        'ACCOUNT_UNIQUE_EMAIL = True\n'
        'ACCOUNT_FORMS = {\n'
        '    "signup": "users.forms.CustomSignupForm",\n'
        '}\n'
        'AUTHENTICATION_BACKENDS = (\n'
        '    "rules.permissions.ObjectPermissionBackend",\n'
        '    "django.contrib.auth.backends.ModelBackend",\n'
        '    "allauth.account.auth_backends.AuthenticationBackend",\n'
        ')\n\n'
        '# EMAIL\n'
        '# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"\n'
        'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"\n'
        'EMAIL_HOST = "smtp.gmail.com"\n'
        'EMAIL_PORT = 587\n'
        f'EMAIL_HOST_USER = "{config["email"]}"\n'
        'EMAIL_HOST_PASSWORD = "password"\n'
        'EMAIL_USE_TLS = True\n'
        'DEFAULT_FROM_EMAIL = EMAIL_HOST_USER\n\n'
        '# django-debug-toolbar config\n'
        'TESTING_MODE = "test" in sys.argv\n'
        'DEV_MODE = DEBUG and not TESTING_MODE\n\n'
        'if DEV_MODE:\n'
        '    INTERNAL_IPS = (\n'
        '        "127.0.0.1",\n'
        '        "localhost",\n'
        '    )\n'
        '    MIDDLEWARE += [\n'
        '        "debug_toolbar.middleware.DebugToolbarMiddleware",\n'
        '    ]\n\n'
        '    INSTALLED_APPS += [\n'
        '        "debug_toolbar",\n'
        '    ]\n\n'
        '    DEBUG_TOOLBAR_PANELS = [\n'
        '        "debug_toolbar.panels.versions.VersionsPanel",\n'
        '        "debug_toolbar.panels.timer.TimerPanel",\n'
        '        "debug_toolbar.panels.settings.SettingsPanel",\n'
        '        "debug_toolbar.panels.headers.HeadersPanel",\n'
        '        "debug_toolbar.panels.request.RequestPanel",\n'
        '        "debug_toolbar.panels.sql.SQLPanel",\n'
        '        "debug_toolbar.panels.staticfiles.StaticFilesPanel",\n'
        '        "debug_toolbar.panels.templates.TemplatesPanel",\n'
        '        "debug_toolbar.panels.cache.CachePanel",\n'
        '        "debug_toolbar.panels.signals.SignalsPanel",\n'
        '        "debug_toolbar.panels.logging.LoggingPanel",\n'
        '        "debug_toolbar.panels.redirects.RedirectsPanel",\n'
        '        "debug_toolbar.panels.profiling.ProfilingPanel",\n'
        '    ]\n\n'
        '    DEBUG_TOOLBAR_CONFIG = {\n'
        '        "INTERCEPT_REDIRECTS": False,\n'
        '        "SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG,  # needed for Docker!\n'
        '    }\n\n'
        '# Deployment to Heroku\n'
        'import dj_database_url\n\n'
        'db_from_env = dj_database_url.config(conn_max_age=500)\n'
        'DATABASES["default"].update(db_from_env)\n\n'
    )

    # Add new content
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            for (key, value) in inserted_content.items():
                if key in line:
                    f_new.write(value)
                    inserted_content.pop(key, None)
                    break
            f_new.write(line)
    os.remove(filename)
    os.rename(temp_name,filename)

    # Replace content and append at end of file
    with open(filename) as f_old, open(temp_name, "w") as f_new:
        for line in f_old:
            for (key, value) in substituted_content.items():
                if key in line:
                    f_new.write(value)
                    substituted_content.pop(key, None)
                    break
            else:
                f_new.write(line)
            if not line.endswith('\n'):
                # This is the last line / end of file
                f_new.write(appended_content)
    os.remove(filename)
    os.rename(temp_name,filename)


def main():
    """Main entry point"""
    config = get_user_configuration()
    update_pyproject_dot_toml(config)
    update_pytest_dot_ini(config)
    create_django_project(config["name"])
    update_manage_dot_py(config)
    update_settings_dot_py(config)


if __name__ == "__main__":
    main()