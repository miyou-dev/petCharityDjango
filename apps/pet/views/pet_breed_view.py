from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

# 序列化
from pet.utils.serializers import PetBreedSerializer
# 模型
from pet.models import PetBreed


class PetBreedView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    retrieve:
      通过ID获取宠物品种

      需要**ID**

    list:
      获取所有宠物品种

      ## race 种族
      - 0: 猫
      - 1: 狗
      ## variety 品种
      - 猫: 短毛 中长毛 长毛
      - 狗: 超小型 小型 中等 大型 很大型
    """

    authentication_classes = []
    pagination_class = None
    queryset = PetBreed.objects.all()
    serializer_class = PetBreedSerializer
    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('race', 'variety')
