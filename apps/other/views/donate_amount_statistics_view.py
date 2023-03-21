from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime, timedelta

# 认证
from utils.authentication import AdministratorAuthentication
# 序列化
from donate.utils.serializers import DonationListInformationSerializer
# 模型
from donate.models import PetDonationList
from user.models import User
# 接口文档简写
from utils.api.schema import CodeDataJsonSchema, JsonSchema, ArrSchema, IntSchema, StringSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


class DonateAmountStatisticsView(APIView):
    authentication_classes = [AdministratorAuthentication]

    @swagger_auto_schema(
        operation_summary='众筹金额最近10天数据统计',
        manual_parameters=[Parameter.admin_token_param()],
        responses={
            HTTP_200_OK: CodeDataJsonSchema(
                data=ArrSchema(
                    '众筹金额最近10天数据统计',
                    items=JsonSchema(
                        properties={
                            'date': StringSchema('时间'),
                            'amount': IntSchema('金额'),
                        }
                    ),
                ),
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        donate_amount_statistics = []
        start_date = datetime.now() + timedelta(days=-10)
        donation_list_may = {}
        for item in PetDonationList.objects.filter(donate_time__gt=start_date).all():
            month = item.donate_time.month
            day = item.donate_time.day
            key = "{:0>2d}-{:0>2d}".format(month, day)
            if key in donation_list_may.keys():
                donation_list_may[key] = donation_list_may[key] + item.amount
            else:
                donation_list_may[key] = item.amount

        for day in range(1, 11):
            _date = start_date + timedelta(days=day)
            month = _date.month
            day = _date.day
            key = "{:0>2d}-{:0>2d}".format(month, day)
            donate_amount_statistics.append({
                'date': key,
                'amount': donation_list_may[key] if key in donation_list_may else 0
            })

        return Response.code_data(200, '成功', donate_amount_statistics)


class DonateAmountTop(GenericViewSet):
    authentication_classes = [AdministratorAuthentication]

    queryset = PetDonationList.objects.all()
    serializer_class = DonationListInformationSerializer
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='众筹金额最近10天Top数据统计',
        manual_parameters=[Parameter.admin_token_param()],
        responses={
            HTTP_200_OK: CodeDataJsonSchema(
                data=ArrSchema(
                    'DonationListInformationSerializer',
                    items=JsonSchema(),
                ),
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        start_date = datetime.now() + timedelta(days=-10)
        queryset = self.get_queryset().filter(donate_time__gt=start_date).order_by("-amount").all()[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response.code_data(200, '成功', serializer.data)


class UserStatistics(APIView):
    authentication_classes = [AdministratorAuthentication]

    @swagger_auto_schema(
        operation_summary='用户数据统计',
        manual_parameters=[Parameter.admin_token_param()],
        responses={
            HTTP_200_OK: CodeDataJsonSchema(
                data=ArrSchema(
                    '众筹金额最近10天数据统计',
                    items=JsonSchema(
                        properties={
                            'sex': StringSchema('性别'),
                            'sexValue': StringSchema('性别中文名'),
                            'count': IntSchema('数量'),
                        }
                    ),
                ),
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        user_count0 = User.objects.filter(sex=0).count()
        user_count1 = User.objects.filter(sex=1).count()
        user_count2 = User.objects.filter(sex=2).count()
        return Response.code_data(200, '成功', [
            {
                'sex': 'secrecy',
                'sexValue': '保密',
                'count': user_count0,
            }, {
                'sex': 'man',
                'sexValue': '男',
                'count': user_count1,
            }, {
                'sex': 'woman',
                'sexValue': '女',
                'count': user_count2,
            },
        ])
