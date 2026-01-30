import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'fake-key-for-standalone-script'
DEBUG = True
INSTALLED_APPS = [
    'data_base.dialogs', 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

USE_TZ = True # Чтобы не было предупреждений о времени