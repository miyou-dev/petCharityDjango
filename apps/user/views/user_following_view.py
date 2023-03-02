from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

# 序列化
from user.utils.serializers import UserFollowingSerializer
# 模型
from user.models import UserFollowing
# 接口文档简写
from utils.api.schema import IntSchema, BoolSchema, JsonSchema, CodeDetailSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


class UserFollowingView(ListModelMixin, GenericViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    filter_backends = (DjangoFilterBackend,)
    # 过滤器
    filterset_fields = ('followers', 'following')

    @swagger_auto_schema(operation_summary='获取关注/粉丝列表')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='关注/取消关注用户',
        operation_description="多次请求不影响结果",
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            properties={
                'cancel': BoolSchema('取消关注/关注 默认（False）关注'),
                'userId': IntSchema('关注用户ID'),

            }
        ), responses={
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        cancel = request.data.get('cancel', False)
        user_id = request.data.get('userId')
        if user and user_id:
            if cancel:
                UserFollowing.objects.filter(followers=user, following_id=user_id).delete()
                return Response.code_detail(200, '取消关注成功')
            else:
                UserFollowing.objects.create(followers=user, following_id=user_id)
                return Response.code_detail(200, '关注成功')
