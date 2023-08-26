import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()
from django.contrib.auth.hashers import make_password
from Database.models import User
import os
import hashlib
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def create_user():
    username = os.getenv('SUPER')
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        password = os.getenv('SUPER_PASSWORD')
        User.objects.create(username=username, password=make_password(password))


if __name__ == '__main__':
    create_user()
