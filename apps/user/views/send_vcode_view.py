from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.throttling import SimpleRateThrottle

from drf_yasg.utils import swagger_auto_schema

# 数据验证
from utils.validation import judge_phone
# 发送验证码
from utils.msg import send_msg

# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, CodeDetailSchema
# 返回简写
from utils.response.response import Response


# 发送验证码
class SendVCodeView(APIView):
    # 频率
    class SendVerificationThrottle(SimpleRateThrottle):
        scope = 'SendVerificationFrequency'

        def get_cache_key(self, request, view):
            return self.get_ident(request)

    authentication_classes = []
    throttle_classes = [SendVerificationThrottle]

    @swagger_auto_schema(
        operation_summary='发送验证码',
        operation_description='目前验证码为手机号码后4位 验证码时限**5分钟**',
        request_body=JsonSchema(
            required=['phone'],
            properties={'phone': StringSchema('手机号码')},
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        if not judge_phone(phone):
            return Response.code_detail(400, '参数错误或者手机号非法')
        if send_msg(phone):
            return Response.code_detail(200, '发送验证码成功')
        else:
            return Response.code_detail(400, '发送验证码失败')
