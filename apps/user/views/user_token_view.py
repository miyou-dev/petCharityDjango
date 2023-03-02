from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from drf_yasg.utils import swagger_auto_schema, no_body

# 工具
from utils.validation import judge_nickname_verify, judge_id_card_verify

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from user.utils.serializers import UserLoginInformationSerializer, UpdateUserSerializer
# 模型
from user.models import User
# 接口文档简写
from utils.api.schema import DetailSchema, JsonSchema, StringSchema, CodeDetailSchema
from utils.api.parameter import Parameter
# 添加功能的 Response
from utils.response.response import Response


class UserTokenView(UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginInformationSerializer
    authentication_classes = [MustLoginAuthentication]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateUserSerializer
        return super().get_serializer_class()

    def get_object(self):
        if self.action == 'partial_update':
            return self.request.user
        return super().get_object()

    # --------------------------------------------------Token获取用户信息--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='Token获取信息',
        manual_parameters=[Parameter.must_token_param()],
        request_body=no_body,
        responses={
            HTTP_200_OK: UserLoginInformationSerializer,
            HTTP_403_FORBIDDEN: DetailSchema.token_err(),
        }
    )
    def information(self, request, *args, **kwargs):
        user_message = self.get_serializer(request.user)
        return Response(user_message.data)

    @swagger_auto_schema(
        operation_summary='修改用户信息',
        operation_description='需要改什么就传什么',
        manual_parameters=[Parameter.must_token_param()],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # --------------------------------------------------用户实名认证--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='用户实名认证',
        operation_description=
        """
         ## code
        - 200:成功
        - 1001: 姓名或身份证号码非法.
        - 1002: 用户已实名认证 无需重复认证.
        """,
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            required=['realName', 'idCard'],
            properties={
                'realName': StringSchema('真实姓名'),
                'idCard': StringSchema('身份证号码'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def authentication(self, request, *args, **kwargs):
        user: User = request.user
        real_name = request.data.get('realName', '')
        id_card = request.data.get('idCard', '')
        if not judge_nickname_verify(real_name) or not judge_id_card_verify(id_card):
            return Response.code_detail(1001, '姓名或身份证号码非法')
        if user.id_card is not None:
            return Response.code_detail(1002, '用户已实名认证 无需重复认证')
        user.real_name = real_name
        user.id_card = id_card
        user.save()
        return Response.code_detail(200, '认证成功')
#
