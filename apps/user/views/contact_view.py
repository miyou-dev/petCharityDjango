from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

# 认证
from utils.authentication import MustLoginAuthentication
# 模型
from user.models import Contact, User
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, CodeDetailSchema
from utils.api.parameter import Parameter
# 返回简写
from utils.response.response import Response


# 发送验证码
class ContactView(APIView):
    authentication_classes = [MustLoginAuthentication]

    @swagger_auto_schema(
        operation_summary='个人联系方式修改',
        manual_parameters=[Parameter.must_token_param()],
        request_body=JsonSchema(
            required=['phone', 'mail', 'qq', 'wechat'],
            properties={
                'phone': StringSchema('手机号码'),
                'mail': StringSchema('邮箱'),
                'qq': StringSchema('QQ'),
                'wechat': StringSchema('微信'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def post(self, request, *args, **kwargs):
        user: User = request.user
        phone = request.data.get('phone', '')
        mail = request.data.get('mail', '')
        qq = request.data.get('qq', '')
        wechat = request.data.get('wechat', '')
        if user.contact is not None:
            user.contact.phone = phone
            user.contact.mail = mail
            user.contact.qq = qq
            user.contact.wechat = wechat
            user.contact.save()
        else:
            contact = Contact.objects.create(phone=phone, mail=mail, qq=qq, wechat=wechat)
            user.contact = contact
            user.save()
        return Response.code_detail(200, '成功')
