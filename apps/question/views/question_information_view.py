from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_yasg.utils import swagger_auto_schema

# 序列化
from question.utils.serializers import QuestionInformationSerializer
# 模型
from question.models import Question


# 问 获取信息
class QuestionInformationView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionInformationSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 过滤器
    filterset_fields = ('classification', 'user')
    # 搜索
    search_fields = ('question',)
    # 排序
    ordering_fields = ('create_time',)

    @swagger_auto_schema(operation_summary='获取问题详情')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='获取问题列表')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
