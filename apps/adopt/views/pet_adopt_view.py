from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import BasePermission

from drf_yasg.utils import swagger_auto_schema

# 认证
from utils.authentication import MustLoginAuthentication
# 序列化
from adopt.utils.serializers import PetAdoptSerializer
# 模型
from pet.models import Pet
from adopt.models import PetAdopt
# 接口文档简写
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


# 宠物领养创建/修改/删除
class PetAdoptView(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    class PetPermission(BasePermission):
        def has_object_permission(self, request, view, adopt: PetAdopt):
            if adopt.pet.user != request.user:
                return False
            return True

        def has_permission(self, request, view):
            if view.action == 'create' or view.action == 'partial_update':
                pet_id = request.data.get('pet', 0)
                if Pet.objects.filter(pk=pet_id, user_id=request.user.id).count() == 0:
                    return False
            return super().has_permission(request, view)

    authentication_classes = [MustLoginAuthentication]
    permission_classes = [PetPermission]
    queryset = PetAdopt.objects.all()
    serializer_class = PetAdoptSerializer

    @swagger_auto_schema(
        operation_summary='创建宠物领养',
        manual_parameters=[Parameter.must_token_param()],
    )
    def create(self, request, *args, **kwargs):
        pet_id = request.data.get('pet', 0)
        if PetAdopt.objects.filter(pet_id=pet_id).count() != 0:
            return Response.code_detail(400, '该宠物已经有一个宠物领养')
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='修改宠物领养信息',
        manual_parameters=[Parameter.must_token_param()],
    )
    def partial_update(self, request, *args, **kwargs):
        pet_id = request.data.get('pet', 0)
        instance: PetAdopt = self.get_object()
        if PetAdopt.objects.filter(pet_id=pet_id).count() != 0 and instance.pet.id != pet_id:
            return Response.code_detail(400, '该宠物已经有一个宠物领养')
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='删除宠物领养',
        manual_parameters=[Parameter.must_token_param()],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
