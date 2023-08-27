from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from Database.models import Article, ArticleDetail
from Serializer import ArticleDetailGETSerializer, ArticleListSerializer, ArticlePostSerializer, \
    ArticleDetailBlockSerializer
from rest_framework.parsers import MultiPartParser
import uuid
from rest_framework.response import Response
from project.settings import ZSET_CLICK_NAME, REDIS_CLIENT
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ArticleView(ModelViewSet):
    queryset = Article.objects.all().order_by('-publish_date')
    serializer_class = ArticleListSerializer
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleListSerializer
        return ArticlePostSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('famous', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得熱門文章傳1，不取得熱門文章傳0'),
    ])
    def list(self, request, *args, **kwargs):
        click_gte_five = REDIS_CLIENT.zrevrangebyscore(ZSET_CLICK_NAME, 'inf', 5, withscores=True)
        if not click_gte_five or request.query_params.get('famous') != '1':
            return super().list(request, *args, **kwargs)
        query_dict = Article.objects.in_bulk(int(click[0]) for click in click_gte_five)
        res = []
        for article in click_gte_five:
            res.append(query_dict[int(article[0])])
        page = self.paginate_queryset(res)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        data = self.get_serializer(res, many=True).data
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(uuid4_hex=uuid.uuid4().hex)

    def perform_destroy(self, instance):
        REDIS_CLIENT.zrem(ZSET_CLICK_NAME, instance.id)
        instance.delete()


class ArticleDetailPostView(ModelViewSet):
    pagination_class = None
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleDetailGETSerializer
        return ArticleDetailBlockSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return Article.objects.select_related('tag').prefetch_related('articledetail_set').filter(
                id=self.kwargs['article_id'])
        return ArticleDetail.objects.all()

    def list(self, request, *args, **kwargs):
        REDIS_CLIENT.zincrby(ZSET_CLICK_NAME, 1, kwargs['article_id'])
        data = super().list(request, *args, **kwargs).data[0]
        data['click'] = int(REDIS_CLIENT.zscore(ZSET_CLICK_NAME, kwargs['article_id']))
        return Response(data)

    def create(self, request, *args, **kwargs):
        if not Article.objects.filter(id=self.kwargs['article_id']).exists():
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.get_queryset().filter(article_id=self.kwargs['article_id'], block=serializer.validated_data['block']).exists():
            raise serializers.ValidationError({'block': [f'{serializer.validated_data["block"]} existed']})
        serializer.save(article_id=self.kwargs['article_id'])
