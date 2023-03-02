from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from datetime import datetime

from django.db.models import Sum

# 用户工具
from user.utils.tools import judge_pay_password, pay

# 认证
from utils.authentication import MustLoginAuthentication
# 模型
from donate.models import PetDonate, PetDonationList
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, IntSchema, CodeDetailSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


class DonationListView(CreateModelMixin, GenericViewSet):
    """
    create:
      捐赠

      ## code
      - 1602:支付密码错误
      - 1603:众筹当前未在进行中
      - 1604:捐赠金额小于0或者大于剩余捐赠金额
      - 1605:余额不足
    """
    queryset = PetDonationList.objects.all()
    authentication_classes = [MustLoginAuthentication]

    # --------------------------------------------------捐赠宠物帮助众筹--------------------------------------------------
    @swagger_auto_schema(
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            properties={
                'donateId': IntSchema('宠物帮助众筹ID'),
                'amount': IntSchema('捐赠金额'),
                'payPassword': StringSchema('支付密码')
            }
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema(detail='捐赠成功'),
        })
    def create(self, request, *args, **kwargs):
        user = request.user
        donate_id = request.data.get('donateId')
        amount = int(request.data.get('amount', 0))
        pay_password = request.data.get('payPassword')
        try:
            # 判断支付密码是否正确
            if not judge_pay_password(user.phone, pay_password):
                return Response.code_detail(1602, '支付密码错误')
            donate: PetDonate = get_object_or_404(PetDonate.objects.all(), pk=donate_id)
            # 判断众筹是否正在进行中
            if donate.state != 1:
                return Response.code_detail(1603, '众筹当前未在进行中')
            # 获取已经众筹的金额
            already_amount_count = self.donation_sum(donate)
            # 判断众筹金额是否正确
            if amount <= 0 or amount > donate.amount - already_amount_count:
                return Response.code_detail(1604, '捐赠金额小于0或者大于剩余捐赠金额')
            # 支付
            if pay(user, amount):
                # 支付成功 创建众筹订单

                donation_item = self.queryset.create(
                    user=user,
                    donate_id=donate_id,
                    amount=amount,
                    order='',
                    remarks='无',
                )
                order = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}{"{:0>6d}".format(donation_item.id % 1000000)}'
                donation_item.order = order
                print(order)
                donation_item.save()
                # 判断众筹是否完成
                if donate.amount == already_amount_count + amount:
                    # 众筹完成
                    donate.state = 2
                    donate.finish_time = datetime.now()
                    donate.save()

                return Response.code_detail(200, '成功')
            else:
                return Response.code_detail(1605, '余额不足')
        except PetDonate.DoesNotExist:
            return Response.code_detail(400, '参数错误')

    # 获取已经众筹的金额
    def donation_sum(self, donate: PetDonate):
        amounts = self.queryset.filter(donate_id=donate.id).aggregate(Sum('amount'))
        return amounts['amount__sum'] if amounts['amount__sum'] else 0


# 发布
def publish(donate: PetDonate):
    donate.state = 1
    donate.save()
