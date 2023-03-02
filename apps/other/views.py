from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from django.db.models import Sum

# 模型
from donate.models import PetDonate
from user.models import User
# 接口文档简写
from utils.api.schema import CodeDataJsonSchema, JsonSchema, IntSchema
# 返回简写
from utils.response.response import Response


class StatisticsView(APIView):
    @swagger_auto_schema(
        operation_summary='数据统计',
        # operation_description="筛选只对donateCount, amount 生效",
        # manual_parameters=[
        #     openapi.Parameter('startDate', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='开始时间'),
        #     openapi.Parameter('endDate', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='结束时间'),
        # ],
        responses={
            HTTP_200_OK: CodeDataJsonSchema(
                data=JsonSchema(
                    properties={
                        'count': IntSchema('返回志愿者人数'),
                        'donateCount': IntSchema('已帮助宝贝人数'),
                        'amount': IntSchema('众筹金额费用累计'),
                    }
                )),
        }
    )
    def get(self, request, *args, **kwargs):
        # start_date = request.GET.get('startDate', '')
        # end_date = request.GET.get('endDate', '')
        count = User.objects.all().count()
        queryset = PetDonate.objects.all()

        donate_count = queryset.count()
        amount = queryset.filter(state=2).aggregate(Sum('amount'))
        return Response.code_data(200, '成功', {
            'count': count,
            'donateCount': donate_count,
            'amount': amount['amount__sum'] if amount['amount__sum'] else 0
        })
