from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, ValidationError

from drf_yasg.utils import swagger_serializer_method

from django.db.models import Sum

from pet.utils.serializers import PetImageSerializer, PetBreedSerializer
from user.utils.serializers import UserPublicInformationSerializer

from donate.models import PetDonate, PetDonationList
from pet.models import PetImage
from user.models import UserCollect


# 返回宠物帮助众筹宠物捐赠名单序列化
class DonationListInformationSerializer(ModelSerializer):
    class Meta:
        model = PetDonationList
        fields = '__all__'

    user = SerializerMethodField(label='用户')

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_user(self, donation_list: PetDonationList):
        return UserPublicInformationSerializer(donation_list.user, context=self.context).data


# 宠物帮助众筹序列化
class DonateSerializer(ModelSerializer):
    class Meta:
        model = PetDonate
        exclude = ['publish_time', 'finish_time']

    breed = SerializerMethodField(label='品种')
    sex_value = CharField(source='get_sex_display', label='性别', read_only=True)
    images = SerializerMethodField(label='图片', read_only=True)
    cover_image = SerializerMethodField(label='封面图片')

    @swagger_serializer_method(serializer_or_field=PetBreedSerializer)
    def get_breed(self, donate: PetDonate):
        return PetBreedSerializer(donate.breed, context=self.context).data

    @swagger_serializer_method(serializer_or_field=PetImageSerializer)
    def get_images(self, donate: PetDonate):
        pet_images = PetImage.objects.filter(FK_donate_image__donate=donate)
        return PetImageSerializer(pet_images, context=self.context, many=True).data

    @swagger_serializer_method(serializer_or_field=PetImageSerializer)
    def get_cover_image(self, donate: PetDonate):
        pet_images = PetImage.objects.filter(FK_donate_image__donate=donate, FK_donate_image__cover=True).first()
        return PetImageSerializer(pet_images, context=self.context).data

    def validate_amount(self, amount):
        if amount < 100:
            raise ValidationError("众筹金额需要大于100!")
        return amount


# 宠物帮助众筹信息序列化
class DonateInformationSerializer(DonateSerializer):
    class Meta:
        model = PetDonate
        exclude = ['admin']
        depth = 1

    donation_list = SerializerMethodField(label='捐赠列表')
    already_amount = SerializerMethodField(label='已筹金额')
    already_people_count = SerializerMethodField(label='众筹人数')
    collect_count = SerializerMethodField(label='收藏人数')
    is_collect = SerializerMethodField(label='是否收藏')

    @swagger_serializer_method(serializer_or_field=DonationListInformationSerializer)
    def get_donation_list(self, donate: PetDonate):
        donate_list = PetDonationList.objects.filter(donate=donate).order_by('-amount')[:10]
        return DonationListInformationSerializer(donate_list, context=self.context, many=True).data

    def get_already_amount(self, donate: PetDonate) -> int:
        already_amount = PetDonationList.objects.filter(donate=donate).aggregate(Sum('amount'))
        return already_amount['amount__sum'] if already_amount['amount__sum'] else 0

    def get_already_people_count(self, donate: PetDonate) -> int:
        return PetDonationList.objects.filter(donate=donate).count()

    def get_collect_count(self, donate: PetDonate) -> int:
        return UserCollect.objects.filter(collect_category=1, collect_id=donate.id).count()

    def get_is_collect(self, donate: PetDonate) -> bool:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return UserCollect.objects.filter(user=request.user, collect_category=1, collect_id=donate.id).exists()
        return False
