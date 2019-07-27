import os
import sys

def start():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webui.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1:
        execute_from_command_line(sys.argv)
    elif len(sys.argv) == 1:
        execute_from_command_line(("managerun.py", "runserver", "0.0.0.0:1136"))

if __name__ == '__main__':
    start()
