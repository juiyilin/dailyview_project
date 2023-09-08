from database.models import Article, ArticleDetail
from rest_framework.serializers import ModelSerializer
from project.settings import MEDIA_PATH


class ArticleListSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'publish_date', 'small_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.small_image:
            data['small_image'] = MEDIA_PATH + instance.small_image.name
        return data


class ArticlePostSerializer(ModelSerializer):
    class Meta:
        model = Article
        exclude = ['uuid4_hex']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.small_image:
            data['small_image'] = MEDIA_PATH + instance.small_image.name
        if instance.main_image:
            data['main_image'] = MEDIA_PATH + instance.main_image.name
        data['tag'] = instance.tag.tag
        return data


class ArticleDetailBlockSerializer(ModelSerializer):

    class Meta:
        model = ArticleDetail
        exclude = ['article']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = MEDIA_PATH + instance.image.name
        return data


class ArticleDetailGETSerializer(ModelSerializer):
    detail = ArticleDetailBlockSerializer(many=True, source='articledetail_set', read_only=True)

    class Meta:
        model = Article
        exclude = ['uuid4_hex']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.small_image:
            data['small_image'] = MEDIA_PATH + instance.small_image.name
        if instance.main_image:
            data['main_image'] = MEDIA_PATH + instance.main_image.name
        data['tag'] = instance.tag.tag
        return data
