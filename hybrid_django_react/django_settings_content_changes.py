def get_settings_dot_py_changes(config):
    """Return dictionaries with changed strings of settings.py"""

    INSERTED = { # Value inserted before line with key
        "from pathlib import Path": "import sys, os\n",
        "# Quick-start development settings": (
            '# Environment flag\n'
            'ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", default="development")\n\n'
        ),
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
            '    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")\n\n'
        ),
        "django.contrib.staticfiles": '    "whitenoise.runserver_nostatic",\n',
        "# Static files (CSS, JavaScript, Images)": (
            "LOCALE_PATHS = [\n"
            "    os.path.join(BASE_DIR, 'locale'),\n"
            "]\n"
            "LANGUAGES = [\n"
            "   ('en-us', 'English'),\n"
            "   ('es', 'Spanish'),\n"
            "]\n\n"
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

    SUBSTITUTED = { # Line with key is substituted with content
        "SECRET_KEY = ": 'SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY",default="django-insecure-@04%uk08cz)mpenm#15f*5zg!0(pnc&p@2pzq6shfwi*%h900f",)\n\n',
        "DEBUG = True": 'DEBUG = os.environ.get("DJANGO_DEBUG", default="True") == "True"\n',
        "ALLOWED_HOSTS = []" : 'ALLOWED_HOSTS = ["localhost","127.0.0.1",]\n',
        "'DIRS': []": '        "DIRS": [str(Path(BASE_DIR, "templates"))],\n',
        "django.contrib.staticfiles":(
            '    "django.contrib.staticfiles",\n'
            '    "django.contrib.sites",\n'
            '    # Third party\n'
            '    "allauth",\n'
            '    "allauth.account",\n'
            '    "rest_framework",\n'
            '    # Local\n'
        ),
        "'django.contrib.sessions.middleware.SessionMiddleware',": (
            "    'whitenoise.middleware.WhiteNoiseMiddleware',\n"
            "    'django.contrib.sessions.middleware.SessionMiddleware',\n"
            "    'django.middleware.locale.LocaleMiddleware',\n"
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

    APPENDED = ( # Content appended to end of file
        '\n\n# Custom User model\n'
        '#AUTH_USER_MODEL = "users.CustomUser"\n\n'
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
        '# Django Rest Framework\n'
        'REST_FRAMEWORK = {\n'
        '    # Use Django standard `django.contrib.auth` permissions,\n'
        '    # or allow read-only access for unauthenticated users.\n'
        '    "DEFAULT_PERMISSION_CLASSES": [\n'
        '        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"\n'
        '    ]\n'
        '}\n\n'
    )

    return (INSERTED, SUBSTITUTED, APPENDED)