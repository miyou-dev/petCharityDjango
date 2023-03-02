from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import BasePermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_403_FORBIDDEN

from drf_yasg.utils import swagger_auto_schema

from django.db.models import Q

# 序列化
from pet.utils.serializers import PetInformationSerializer
# 模型
from pet.models import Pet
# 接口文档简写
from utils.api.schema import DetailSchema
from utils.api.parameter import Parameter


# 宠物 获取信息
class PetInformationView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    class PetInformationPermission(BasePermission):
        def has_object_permission(self, request, view, pet):
            if not pet.visual and pet.user != request.user:
                return False
            return True

    permission_classes = [PetInformationPermission]
    queryset = Pet.objects.all()
    serializer_class = PetInformationSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 过滤器
    filterset_fields = ('user', 'breed', 'sex')
    # 搜索
    search_fields = ('name',)
    # 排序
    ordering_fields = ('create_time',)

    def get_queryset(self):
        if self.action == 'list':
            return super().get_queryset().filter(Q(visual=True) | Q(user=self.request.user))
        return super().get_queryset()

    # --------------------------------------------------获取宠物详情--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='获取宠物详情',
        operation_description='无token时需要宠物为公开状态才能访问',
        manual_parameters=[Parameter.token_param()],
        responses={
            HTTP_403_FORBIDDEN: DetailSchema('宠物状态不可见'),
        })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # --------------------------------------------------获取宠物列表--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='获取宠物列表',
        operation_description='有**token**时可以访问自己私有的宠物 无**token**时获取用户公开宠物',
        manual_parameters=[
            Parameter.token_param(),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
