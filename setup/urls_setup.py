import os


def change_project_urls(config):
    """Overwrite project's urls.py file"""
    filename = f"{config['name']}/urls.py"
    temp_name = f"{filename}_new.txt"

    with open(temp_name, "w") as f:
        f.write(
            'from django.conf import settings\n'
            'from django.contrib import admin\n'
            'from django.urls import path, include\n\n'
            'import debug_toolbar\n\n'
            'from users.views import CustomLoginView\n\n'
            'urlpatterns = [\n'
            '    # Django admin:\n'
            '    path("ceoenterpreneurbornin1964/", admin.site.urls),\n'
            '    # User management:\n'
            '    path("accounts/", include("allauth.urls")),\n'
            '    # Local apps:\n'
            '    path("", include("pages.urls", namespace="pages")),\n'
            '    path("accounts/", include("users.urls", namespace="users")),\n'
            '    path("app/", include("chores.urls", namespace="app")),\n'
            ']\n\n'
            'if settings.DEV_MODE:\n'
            '    import debug_toolbar\n\n'
            '    urlpatterns = [\n'
            '        path("__debug__/", include(debug_toolbar.urls)),\n'
            '    ] + urlpatterns\n'
        )

    os.remove(filename)
    os.rename(temp_name,filename)
