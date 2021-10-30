import random
import os
import string


def change_project_urls(config):
    """Overwrite project's urls.py file"""
    filename = f"{config['name']}/urls.py"
    temp_name = f"{filename}_new.txt"

    random_admin_url = (
        ''.join(random.SystemRandom()
        .choice(string.ascii_letters + string.digits)
         for _ in range(20)))

    with open(temp_name, "w") as f:
        f.write(
            'from django.conf import settings\n'
            'from django.contrib import admin\n'
            'from django.urls import path, include\n'
            'from django.views.generic import TemplateView\n\n'
            'import debug_toolbar\n\n'
            'urlpatterns = [\n'
            '    # Django admin:\n'
            f'    path("{random_admin_url}/", admin.site.urls),\n'
            '    # User management:\n'
            '    #path("accounts/", include("allauth.urls")),\n'
            '    # Local apps:\n'
            '    path("", TemplateView.as_view(template_name="index.html")),\n'
            ']\n\n'
            'if settings.DEV_MODE:\n'
            '    import debug_toolbar\n\n'
            '    urlpatterns = [\n'
            '        path("__debug__/", include(debug_toolbar.urls)),\n'
            '    ] + urlpatterns\n'
        )

    os.remove(filename)
    os.rename(temp_name,filename)
