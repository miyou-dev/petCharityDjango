from rest_framework.views import APIView
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema


# 认证
from utils.authentication import MustLoginAuthentication
# 模型
from user.models import UserCollect
# 接口文档简写
from utils.api.schema import JsonSchema, IntSchema, BoolSchema, CodeDetailSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


# 收藏
class UserCollectView(APIView):
    authentication_classes = [MustLoginAuthentication]

    @swagger_auto_schema(
        operation_summary='收藏',
        operation_description="多次请求不影响结果",
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            properties={
                'cancel': BoolSchema('取消收藏/收藏 默认（False）收藏'),
                'collectId': IntSchema('收藏ID'),
                'collectCategory': IntSchema('收藏类别 (1, 众筹), (2, 领养)')
            }
        ),
        responses={
            status.HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        cancel = request.data.get('cancel', False)
        collect_id = request.data.get('collectId')
        collect_category = request.data.get('collectCategory')
        if user and collect_id and collect_category:
            if cancel:
                UserCollect.objects.filter(user=user, collect_id=collect_id, collect_category=collect_category).delete()
                return Response.code_detail(200, '取消收藏成功')
            else:
                UserCollect.objects.create(user=user, collect_id=collect_id, collect_category=collect_category)
                return Response.code_detail(200, '收藏成功')
