from project.settings import TIMEOUT
from django.core.cache import caches
from rest_framework_simplejwt.views import TokenBlacklistView
from api.tool.authentication import MyJWTAuthentication


class JWTLogout(TokenBlacklistView):
    """
    登出
    """
    authentication_classes = [MyJWTAuthentication]

    def post(self, request, *args, **kwargs):
        caches['token'].set(request.auth.token, 1, TIMEOUT)
        return super().post(request, *args, **kwargs)
