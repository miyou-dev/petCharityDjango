from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import BasePermission

from drf_yasg.utils import swagger_auto_schema

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from question.utils.serializers import AnswerSerializer
# 模型
from question.models import Answer
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, IntSchema
from utils.api.parameter import Parameter


# 答 创建/修改/删除
class AnswerView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    class AnswerPermission(BasePermission):
        def has_object_permission(self, request, view, answer: Answer):
            if answer.user != request.user:
                return False
            return True

    authentication_classes = [MustLoginAuthentication]
    permission_classes = [AnswerPermission]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    properties = {
        'question': IntSchema('问题'),
        'answer': StringSchema('答案'),
    }

    @swagger_auto_schema(
        operation_summary='创建问题答案',
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            required=['question', 'answer'],
            properties=properties
        )
    )
    def create(self, request, *args, **kwargs):
        # 写入用户信息
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='删除问题答案',
        manual_parameters=[Parameter.must_token_param()],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
