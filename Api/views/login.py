# from Serializer import CustomTokenSerializer, LogoutSerializer
from rest_framework.views import APIView
from project.settings import TIMEOUT
import random
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
# from PIL import Image, ImageDraw
from django.core.cache import caches
import base64
import jwt
from io import BytesIO
# from Admin.permissions import IsLoginUser
from rest_framework import serializers, status
from rest_framework_simplejwt.views import TokenBlacklistView
from Tool.authentication import MyJWTAuthentication

# class TokenView(TokenObtainPairView):
#     """
#     登入
#     *** 密碼在傳送到後端前請先以MD5方式雜湊 ***
#     """
#     serializer_class = CustomTokenSerializer
#     permission_classes = []


class Test(APIView):
    def get(self, request):
        return Response({'aaa': 222})


class JWTLogout(TokenBlacklistView):
    """
    登出
    """
    authentication_classes = [MyJWTAuthentication]

    def post(self, request, *args, **kwargs):
        caches['token'].set(request.auth.token, 1, TIMEOUT)
        return super().post(request, *args, **kwargs)
