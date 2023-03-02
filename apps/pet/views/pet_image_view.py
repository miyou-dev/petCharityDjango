from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg.openapi import Parameter, IN_FORM, TYPE_FILE

from django.http import HttpResponse


# 序列化
from pet.utils.serializers import PetImageSerializer
# 模型
from pet.models import PetImage
# 接口文档简写
from utils.api.schema import FileSchema
# 返回简写
from utils.response.response import Response


# 宠物图片 获取 创建
class PetImageView(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """
    retrieve:
      通过ID获取宠物图片URL

      无
    """

    queryset = PetImage.objects.all()
    serializer_class = PetImageSerializer
    parser_classes = [MultiPartParser]

    # --------------------------------------------------上传宠物图片 - -------------------------------------------------
    @swagger_auto_schema(
        operation_summary='上传宠物图片',
        manual_parameters=[
            Parameter('image', IN_FORM, type=TYPE_FILE, description='宠物图片文件'),
        ],
        request_body=no_body,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image: PetImage = serializer.save()
        image.width = image.image.width
        image.height = image.image.height
        image.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary='通过ID获取宠物图片',
        responses={
            HTTP_200_OK: FileSchema(),
        })
    def get(self, request, *args, **kwargs):
        pet_image: PetImage = self.get_object()
        file = pet_image.image.read()
        return HttpResponse(file, content_type='image/png')
