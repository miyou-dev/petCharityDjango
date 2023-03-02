from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter

# 序列化
from adopt.utils.serializers import PetAdoptInformationSerializer
# 模型
from adopt.models import PetAdopt


# 宠物领养查看
class PetAdoptInformationView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    retrieve:
      获取领养详情

      无
    list:
      获取领养列表

      无
    """

    class PetAdoptInformationServerFilter(FilterSet):
        class Meta:
            model = PetAdopt
            fields = ['pet__user', 'pet__breed', 'pet__sex']

        startWeight = NumberFilter(field_name='pet__weight', lookup_expr='gte')
        endWeight = NumberFilter(field_name='pet__weight', lookup_expr='lte')

    queryset = PetAdopt.objects.all()
    serializer_class = PetAdoptInformationSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 过滤器
    filterset_class = PetAdoptInformationServerFilter
    # 搜索
    search_fields = ('title', 'description', 'requirements', 'pet__user__nickname')
    # 排序
    ordering_fields = ('create_time',)
