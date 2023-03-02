from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from drf_yasg.utils import swagger_serializer_method

from user.utils.serializers import UserPublicInformationSerializer

from pet.models import PetBreed, PetImage, Pet


# 宠物图片序列化
class PetBreedSerializer(ModelSerializer):
    class Meta:
        model = PetBreed
        fields = "__all__"


# 宠物图片序列化
class PetImageSerializer(ModelSerializer):
    class Meta:
        model = PetImage
        fields = '__all__'


# 宠物序列化
class PetSerializer(ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

    sex_value = CharField(source='get_sex_display', label='性别', read_only=True)
    images = SerializerMethodField(label='图片')
    cover_image = SerializerMethodField(label='封面图片')

    @swagger_serializer_method(serializer_or_field=PetImageSerializer)
    def get_images(self, pet: Pet):
        pet_images = PetImage.objects.filter(FK_pet_image__pet=pet)
        return PetImageSerializer(pet_images, context=self.context, many=True).data

    @swagger_serializer_method(serializer_or_field=PetImageSerializer)
    def get_cover_image(self, pet: Pet):
        pet_images = PetImage.objects.filter(FK_pet_image__pet=pet, FK_pet_image__cover=True).first()
        return PetImageSerializer(pet_images, context=self.context).data


# 宠物信息序列化
class PetInformationSerializer(PetSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        depth = 1

    user = SerializerMethodField(label='用户')

    @swagger_serializer_method(serializer_or_field=UserPublicInformationSerializer)
    def get_user(self, pet: Pet):
        return UserPublicInformationSerializer(pet.user, context=self.context).data
