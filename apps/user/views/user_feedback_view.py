from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter

# 认证
from utils.authentication import AdministratorAuthentication
# 序列化
from user.utils.serializers import UserFeedbackSerializer
# 模型
from user.models import UserFeedback
# 接口文档简写
from utils.api.parameter import Parameter


class UserFeedbackView(CreateModelMixin, GenericViewSet):
    """
    create:
      创建反馈

      无
    """

    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer


class AdminUserFeedbackView(ListModelMixin, DestroyModelMixin, GenericViewSet):
    authentication_classes = [AdministratorAuthentication]

    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer
    filter_backends = (SearchFilter,)
    # 搜索
    search_fields = ('title', 'content')

    @swagger_auto_schema(
        operation_summary='获取全部用户反馈',
        manual_parameters=[Parameter.admin_token_param()],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='删除用户反馈',
        manual_parameters=[Parameter.admin_token_param()],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
