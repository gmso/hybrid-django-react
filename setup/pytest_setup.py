import re


def setup_pytest(config):
    """Entry point of module"""
    update_pytest_dot_ini(config)


def update_pytest_dot_ini(config):
    filename = "pytest.ini"
    with open(filename) as f:
        content = f.read()
    content = re.sub(r'(PROJECT)', f'{config["name"]}', content)
    with open(filename, 'w') as f:
        f.write(content)
