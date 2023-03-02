from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user.models import User
from administrator.models import Administrator


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', None)
        if token:
            user = User.objects.filter(token=token).first()
            if user:
                print(f'UserAuthentication 用户 {user}')
                return user, 200
        print('UserAuthentication 没有token')
        return None, 0


class MustLoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', None)
        if token:
            user = User.objects.filter(token=token).first()
            if user:
                print(f'MustLoginAuthentication 用户 {user}')
                return user, 200
        print('MustLoginAuthentication 禁止访问')
        raise AuthenticationFailed('禁止访问')


class AdministratorAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', None)
        if token:
            admin = Administrator.objects.filter(token=token).first()
            if admin:
                print(f'AdministratorAuthentication 管理员 {admin}')
                return admin, 200
        print('AdministratorAuthentication 禁止访问')
        raise AuthenticationFailed('禁止访问')
