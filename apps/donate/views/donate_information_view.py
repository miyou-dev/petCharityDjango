from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_yasg.utils import swagger_auto_schema

# 序列化
from donate.utils.serializers import DonateInformationSerializer
# 过滤器
from django_filters import rest_framework
# 模型
from donate.models import PetDonate
# 接口文档简写
from utils.api.parameter import Parameter


# 宠物帮助众筹 获取信息
class DonateInformationView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = PetDonate.objects.all()
    serializer_class = DonateInformationSerializer

    filter_backends = (rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 过滤器
    filterset_fields = ('state', 'breed', 'sex')
    # 搜索
    search_fields = ('name', 'description')
    # 排序
    ordering_fields = ('publish_time', 'finish_time', 'amount')

    @swagger_auto_schema(
        operation_summary='获取宠物帮助众筹详情',
        manual_parameters=[Parameter.token_param()],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='获取宠物帮助众筹列表',
        manual_parameters=[Parameter.token_param()],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
