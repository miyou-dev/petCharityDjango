from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from user.utils.serializers import UserImageSerializer
# 模型
from user.models import User
# 接口文档简写
from utils.api.parameter import Parameter


# 用户头像上传
class UserImageView(UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserImageSerializer
    authentication_classes = [MustLoginAuthentication]
    parser_classes = [MultiPartParser]

    # --------------------------------------------------用户头像上传--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='用户头像上传',
        manual_parameters=[Parameter.must_token_param()],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_object(self):
        if self.action == 'partial_update':
            return self.request.user
        return super().get_object()
