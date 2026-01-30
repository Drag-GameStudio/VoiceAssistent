import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Настройка окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_base.settings")
django.setup()