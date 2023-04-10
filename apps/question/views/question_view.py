from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import BasePermission

from drf_yasg.utils import swagger_auto_schema

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from question.utils.serializers import QuestionSerializer
# 模型
from question.models import Question
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, IntSchema
from utils.api.parameter import Parameter


# 问 创建/修改/删除
class QuestionView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    class QuestionPermission(BasePermission):
        def has_object_permission(self, request, view, question: Question):
            if question.user != request.user:
                return False
            return True

    authentication_classes = [MustLoginAuthentication]
    permission_classes = [QuestionPermission]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    properties = {
        'classification': IntSchema('分类'),
        'question': StringSchema('问题'),
    }

    @swagger_auto_schema(
        operation_summary='创建问题',
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            required=['classification', 'question'],
            properties=properties
        )
    )
    def create(self, request, *args, **kwargs):
        # 写入用户信息
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='修改问题',
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(properties=properties)
    )
    def partial_update(self, request, *args, **kwargs):
        # 写入用户信息
        request.data['user'] = request.user.id
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='删除问题',
        manual_parameters=[Parameter.must_token_param()],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
