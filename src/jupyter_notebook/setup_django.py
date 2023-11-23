import os
import sys
import django

DJANGO_SETTINGS_MODULE = "dpthome.settings"

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)

def init():
    os.chdir(parent_directory)
    sys.path.insert(0,  parent_directory)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()