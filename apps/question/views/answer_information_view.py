from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_yasg.utils import swagger_auto_schema

# 序列化
from question.utils.serializers import AnswerInformationSerializer
# 模型
from question.models import Answer


# 问 获取信息
class AnswerInformationView(ListModelMixin, GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerInformationSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 过滤器
    filterset_fields = ('question', 'user')
    # 搜索
    search_fields = ('answer',)
    # 排序
    ordering_fields = ('create_time',)

    @swagger_auto_schema(operation_summary='获取问题答案列表')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
