try:
    # Getting the settings from django
    from django.conf import settings
except (ImportError, ImportError):
    # getting the settings from the local local_settings.py file
    from vosfactures.local_settings import *
else:
    HOST = settings.VOSFACTURES_HOST
    API_TOKEN = settings.VOSFACTURES_API_TOKEN
    AVAILABLE_COMMANDS = settings.VOSFACTURES_AVAILABLE_COMMANDS
