from rest_framework.serializers import ModelSerializer, SerializerMethodField

from drf_yasg.utils import swagger_serializer_method

from pet.utils.serializers import PetInformationSerializer

from user.models import UserCollect
from adopt.models import PetAdopt


# 创建/修改 宠物领养序列化
class PetAdoptSerializer(ModelSerializer):
    class Meta:
        model = PetAdopt
        fields = ['pet', 'title', 'description', 'requirements']


# 返回宠物领养信息序列化
class PetAdoptInformationSerializer(ModelSerializer):
    class Meta:
        model = PetAdopt
        fields = '__all__'

    pet = SerializerMethodField(label='宠物')
    collect_count = SerializerMethodField(label='收藏人数')
    is_collect = SerializerMethodField(label='是否收藏')

    @swagger_serializer_method(serializer_or_field=PetInformationSerializer)
    def get_pet(self, pet_adopt):
        return PetInformationSerializer(pet_adopt.pet, context=self.context).data

    def get_collect_count(self, adopt: PetAdopt) -> int:
        return UserCollect.objects.filter(collect_category=2, collect_id=adopt.id).count()

    def get_is_collect(self, adopt: PetAdopt) -> bool:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserCollect.objects.filter(user=request.user, collect_category=2, collect_id=adopt.id).exists()
        return False
