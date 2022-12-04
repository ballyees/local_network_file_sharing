from django import setup
setup() # fix Django AppRegistryNotReady: Apps aren't loaded yet. in gunicorn
from .file import *