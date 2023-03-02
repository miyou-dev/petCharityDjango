from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import BasePermission

from drf_yasg.utils import swagger_auto_schema

from django.db import IntegrityError

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from pet.utils.serializers import PetSerializer
# 模型
from pet.models import Pet, PetImageMap
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, IntSchema, BoolSchema, ArrSchema, DateSchema, DoubleSchema
from utils.api.parameter import Parameter


# 宠物  创建 修改信息 删除
class PetView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    class PetPermission(BasePermission):
        def has_object_permission(self, request, view, pet: Pet):
            if pet.user != request.user:
                return False
            return True

    authentication_classes = [MustLoginAuthentication]
    permission_classes = [PetPermission]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    properties = {
        'name': StringSchema('名字'),
        'breed': IntSchema('品种'),
        'sex': IntSchema('性别 0公, 1母'),
        'weight': DoubleSchema('体重'),
        'birth': DateSchema('出生日期'),
        'visual': BoolSchema('是否别人可见'),
        'images': ArrSchema('图片id列表', items=IntSchema('图片id')),
        'cover_image': IntSchema('默认图片ID'),
    }

    # --------------------------------------------------创建宠物--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='创建宠物',
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            required=['name', 'breed', 'sex', 'weight', 'birth', 'visual', 'images'],
            properties=properties
        )
    )
    def create(self, request, *args, **kwargs):
        # 写入用户信息
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pet = serializer.save()
        # 获取图片id列表
        image_list = self.request.data.get('images', [])
        # 获取默认图片
        cover_image = self.request.data.get('cover_image', 0)
        if cover_image == 0 or cover_image not in image_list:
            cover_image = image_list[0]

        for item in image_list:
            try:
                PetImageMap.objects.create(pet=pet, image_id=item, cover=item == cover_image).save()
            except IntegrityError:
                print('宠物图片ID错误')

    # --------------------------------------------------修改宠物信息--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='修改宠物信息',
        operation_description="## 需要改什么就传什么",
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(properties=properties)
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        pet = serializer.save()
        if 'images' in self.request.data:
            # 获取图片id列表
            image_list: [str] = self.request.data.get('images', [])
            # 获取默认图片
            cover_image = self.request.data.get('cover_image', 0)
            if len(image_list) == 0:
                return
            if cover_image == 0 or cover_image not in image_list:
                cover_image = image_list[0]

            PetImageMap.objects.filter(pet=pet).delete()
            for item in image_list:
                try:
                    PetImageMap.objects.create(pet=pet, image_id=item, cover=item == cover_image).save()
                except IntegrityError:
                    print('宠物图片ID错误')

    # --------------------------------------------------删除宠物--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='删除宠物',
        manual_parameters=[Parameter.must_token_param()],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
