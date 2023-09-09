from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.translation import gettext_lazy as _
from django.core.cache import caches
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.contrib.auth.hashers import check_password
from api.models import User


class MyCustomBackend(AllowAllUsersModelBackend):
    """
    登入用
    """

    def authenticate(self, request, username, password, **kwargs):
        try:
            user_model = User.objects.get(username=username)
        except Exception as error:
            print(f'{"*" * 10} MyCustomBackend: {error}! {"*" * 10}')
            return None
        if check_password(password=password, encoded=user_model.password):
            return user_model
        else:
            return None


class MyJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:

                str_token = AuthToken(raw_token)
                if caches['token'].get(str(raw_token)):
                    raise InvalidToken({
                        'detail': _('Given token not valid for any token type'),
                        'messages': 'logout token',
                    })
                return str_token
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })
