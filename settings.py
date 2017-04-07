try:
    # Getting the settings from django
    from django.conf.settings import VOSFACTURES_HOST, VOSFACTURES_API_TOKEN
except ImportError:
    # getting the settings from the local local_settings.py file
    from local_settings import *
else:
    HOST = VOSFACTURES_HOST
    API_TOKEN = VOSFACTURES_API_TOKEN