from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.serializers import ModelSerializer

# 过滤器
from django_filters import rest_framework
# 模型
from address.models import Province, City, Area


class AddressView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    pagination_class = None


# 省
class ProvinceView(AddressView):
    """
    retrieve:
      通过id获取指定省信息

      ~~~
      43 湖南
      ~~~

    list:
      获取全部省信息

      无
    """

    class ProvinceSerializer(ModelSerializer):
        class Meta:
            model = Province
            fields = "__all__"

    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


# 市
class CityView(AddressView):
    """
    retrieve:
      通过id获取指定市信息

      ~~~
      4306 岳阳市
      ~~~

    list:
      根据省ID获取所有市信息

      ~~~
      43 湖南省
      ~~~
    """

    class CitySerializer(ModelSerializer):
        class Meta:
            model = City
            fields = "__all__"
            depth = 1

    queryset = City.objects.all()
    serializer_class = CitySerializer
    # 过滤器
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ('belong_province',)


# 区
class AreaView(AddressView):
    """
    retrieve:
      通过id获取指定区信息

      ~~~
      430602 岳阳楼区
      ~~~

    list:
      根据市ID获取所有区信息

      ~~~
      4306 岳阳市
      ~~~
    """

    class AreaSerializer(ModelSerializer):
        class Meta:
            model = Area
            fields = "__all__"
            depth = 2

    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    # 过滤器
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ('belong_city',)
