from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import OrderingFilter

from drf_yasg.utils import swagger_auto_schema

# 序列化
from donate.utils.serializers import DonationListInformationSerializer
# 模型
from donate.models import PetDonationList


class DonationListInformationView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    queryset = PetDonationList.objects.all()
    serializer_class = DonationListInformationSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 过滤器
    filterset_fields = ['user', 'donate']
    # 排序
    ordering_fields = ('donate_time', 'donation')

    @swagger_auto_schema(operation_summary='获取宠物帮助众筹宠物捐赠名单信息')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='获取所有宠物帮助众筹宠物捐赠名单信息')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
