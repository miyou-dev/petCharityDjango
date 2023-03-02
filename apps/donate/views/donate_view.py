from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from drf_yasg.utils import swagger_auto_schema

from django.db import IntegrityError

# 认证
from utils.authentication import AdministratorAuthentication
# 序列化
from donate.utils.serializers import DonateSerializer
# 模型
from donate.models import PetDonate, PetDonateImageMap
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, IntSchema, CodeDetailSchema, ArrSchema, DateSchema, DoubleSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


# 宠物帮助众筹
class DonateView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    authentication_classes = [AdministratorAuthentication]
    queryset = PetDonate.objects.all()
    serializer_class = DonateSerializer

    properties = {
        'name': StringSchema('宠物名称'),
        'breed': IntSchema('品种'),
        'sex': IntSchema('宠物性别'),
        'weight': DoubleSchema('体重'),
        'birth': DateSchema('宠物出生年日'),
        'description': StringSchema('详情'),
        'amount': IntSchema('众筹金额'),
        'images': ArrSchema('图片id列表', items=IntSchema('图片id')),
        'cover_image': IntSchema('默认图片ID'),
    }

    # --------------------------------------------------创建宠物帮助众筹--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='创建宠物帮助众筹',
        manual_parameters=[Parameter.admin_token_param()],
        request_body=JsonSchema(
            required=['name', 'breed', 'sex', 'weight', 'birth', 'description',
                      'amount', 'publish_time', 'images'],
            properties=properties
        )
    )
    def create(self, request, *args, **kwargs):
        request.data['admin'] = request.user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        donate = serializer.save()
        # 获取图片id列表
        image_list = self.request.data.get('images', [])
        # 获取默认图片
        cover_image = self.request.data.get('cover_image', 0)
        if cover_image == 0 or cover_image not in image_list:
            cover_image = image_list[0]

        for item in image_list:
            try:
                PetDonateImageMap.objects.create(donate=donate, image_id=item, cover=item == cover_image).save()
            except IntegrityError:
                print('宠物帮助众筹图片ID错误')

    # --------------------------------------------------修改宠物帮助众筹信息--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='修改宠物帮助众筹信息',
        operation_description="""
        ## 需要改什么就传什么
        
        ## code
        - 200: 成功
        - 1601: 众筹已经开始 无法修改
        """,
        manual_parameters=[Parameter.admin_token_param()],
        request_body=JsonSchema(properties=properties)
    )
    def partial_update(self, request, *args, **kwargs):
        donate = self.get_object()
        # 判断当前是否可以修改
        if donate.state != 0:
            return Response.code_detail(1601, '众筹已经开始 无法修改')
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        donate = serializer.save()
        if 'images' in self.request.data:
            # 获取图片id列表
            image_list: [str] = self.request.data.get('images', [])
            # 获取默认图片
            cover_image = self.request.data.get('cover_image', 0)
            if len(image_list) == 0:
                return
            if cover_image == 0 or cover_image not in image_list:
                cover_image = image_list[0]

            PetDonateImageMap.objects.filter(donate=donate).delete()
            for item in image_list:
                try:
                    PetDonateImageMap.objects.create(donate=donate, image_id=item, cover=item == cover_image).save()
                except IntegrityError:
                    print('宠物帮助众筹图片ID错误')

    # --------------------------------------------------删除宠物帮助众筹--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='删除宠物帮助众筹',
        operation_description="""
        ## code
        - 1601 众筹已经开始 无法删除
        """,
        manual_parameters=[Parameter.admin_token_param()],
        responses={
            HTTP_204_NO_CONTENT: '删除成功',
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def destroy(self, request, *args, **kwargs):
        donate = self.get_object()
        # 判断当前是否可以删除
        if donate.state != 0:
            return Response.code_detail(1601, '众筹已经开始 无法删除')
        self.perform_destroy(donate)
        return Response(status=HTTP_204_NO_CONTENT)
