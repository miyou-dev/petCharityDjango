from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from django.db.models import Sum, Q

# 模型
from donate.models import PetDonate, PetDonationList
from user.models import User
# 接口文档简写
from utils.api.schema import CodeDataJsonSchema, JsonSchema, IntSchema
# 返回简写
from utils.response.response import Response


class UserStatisticsView(APIView):
    @swagger_auto_schema(
        operation_summary='普通用户数据统计',
        responses={
            HTTP_200_OK: CodeDataJsonSchema(
                data=JsonSchema(
                    properties={
                        'userCount': IntSchema('用户数'),
                        'donateCount': IntSchema('众筹宠物数'),
                        'donateAmount': IntSchema('众筹金额费用累计'),
                    }
                )),
        }
    )
    def get(self, request, *args, **kwargs):
        user_count = User.objects.count()
        donate_count = PetDonate.objects.filter(Q(state=1) | Q(state=2)).count()
        donate_amount = PetDonationList.objects.aggregate(Sum('amount'))

        return Response.code_data(200, '成功', {
            'userCount': user_count,
            'donateCount': donate_count,
            'donateAmount': donate_amount['amount__sum'] if donate_amount['amount__sum'] else 0,
        })
