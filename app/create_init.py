import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()
from django.contrib.auth.hashers import make_password
from popular.models import User, CategoryTag
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def create_user():
    username = os.getenv('SUPER')
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        password = os.getenv('SUPER_PASSWORD')
        User.objects.create(username=username, password=make_password(password))


def create_tags():
    tags_list = []
    if CategoryTag.objects.count() == 0:
        for tag in ['熱門', '時事', '政治', '娛樂', '網紅', '生活', '美食', '旅遊', '兩性', '寵物', 'ACG', '產經', '運動']:
            tags_list.append(CategoryTag(tag=tag))
        CategoryTag.objects.bulk_create(tags_list)


if __name__ == '__main__':
    create_user()
    create_tags()
