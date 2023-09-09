from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from popular.models import User


class IsAlive(APIView):
    authentication_classes = []
    permission_classes = []
    swagger_schema = None

    def get(self, request):
        try:
            cache.get('test')  # redis.exceptions.ConnectionError
        except Exception as e:
            return Response({'redis_error': str(e)})
        try:
            User.objects.count()
        except Exception as e:
            return Response({'postgresql_error': str(e)})
        return Response({'result': 'redis, postgresql, server alive'})
