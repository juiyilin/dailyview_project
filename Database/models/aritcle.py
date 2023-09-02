from django.db import models
import time


def small_image_path(instance, filename):
    now = int(time.time())
    return f'article/{instance.uuid4_hex}/s-{now}-{filename}'


def main_image_path(instance, filename):
    now = int(time.time())
    return f'article/{instance.uuid4_hex}/m-{now}-{filename}'


def article_block_image_path(instance, filename):
    now = int(time.time())
    return f'article/{instance.article.uuid4_hex}/b{instance.block}-{now}-{filename}'


class CategoryTag(models.Model):
    tag = models.CharField(max_length=16)

    class Meta:
        db_table = 'CategoryTag'


class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='標題')
    summary = models.CharField(max_length=128, verbose_name='摘要')
    tag = models.ForeignKey(CategoryTag, on_delete=models.CASCADE, verbose_name='標籤')
    small_image = models.ImageField(upload_to=small_image_path, verbose_name='小圖')
    main_image = models.ImageField(upload_to=main_image_path, verbose_name='大圖')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='發佈日期')
    uuid4_hex = models.CharField(max_length=32, verbose_name='資料夾名稱')

    class Meta:
        db_table = 'Article'


class ArticleDetail(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    block = models.PositiveSmallIntegerField(verbose_name='區塊')
    title = models.CharField(max_length=32, verbose_name='標題')
    content = models.TextField(verbose_name='內容')
    image = models.ImageField(upload_to=article_block_image_path, null=True, verbose_name='圖')

    class Meta:
        db_table = 'ArticleDetail'
        ordering = ['block']
