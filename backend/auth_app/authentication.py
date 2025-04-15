from datetime import datetime

import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.request import Request
from django.contrib.auth.models import AnonymousUser
import jwt

from auth_app.models import User


# Авторизационный бэкенд, через него проверяется пользователь и токен 
class JWTAuthectication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        token = authentication.get_authorization_header(request)

        if not token:
            return (AnonymousUser(), "")
            # raise exceptions.AuthenticationFailed("token wasn't provided")
        
        token = token.decode().split(' ')

        if len(token) == 1 or len(token) > 2:
            return (AnonymousUser(), "")
            # raise exceptions.ValidationError("invalid authorization header")
        
        token = token[1]

        encoded = None

        try:
            encoded: dict = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms="HS256"     
            )
        except:
            raise exceptions.AuthenticationFailed("invalid token")


        id = encoded.get("id")
        exp = encoded.get("exp")

        if exp < int(timezone.now().timestamp()):
            raise exceptions.AuthenticationFailed("invalid token")

        try:
            user = User.objects.get(id=id)
            return (user, user.token)
        except:
            raise exceptions.AuthenticationFailed("invalid user")
