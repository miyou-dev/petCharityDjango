from drf_yasg import openapi


class Parameter(openapi.Parameter):
    @staticmethod
    def token_param():
        return Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户Token')

    @staticmethod
    def must_token_param():
        return Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户Token', required=True)

    @staticmethod
    def admin_token_param():
        return Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员Token', required=True)
