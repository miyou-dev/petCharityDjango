from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

# 数据验证
from utils.validation import judge_phone, judge_password_verify
# token
from utils.token import create_token
# 验证码功能
from utils.msg import judge_msg
# 密码加密
from utils.sha1 import pass_en

# 接口文档简写
from utils.api.schema import CodeDetailSchema, JsonSchema, StringSchema, CodeDataJsonSchema
# 模型
from administrator.models import Administrator
# 返回简写
from utils.response.response import Response


class AdminUserView(GenericViewSet):
    # 列化类
    class AdminLoginSerializers(ModelSerializer):
        class Meta:
            model = Administrator
            exclude = ['password']

    queryset = Administrator.objects.all()
    serializer_class = AdminLoginSerializers

    # --------------------------------------------------登录--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='登录',
        operation_description="""
            ## 返回用户信息
            ### code
            - 200: 成功.
            - 204: 手机号、密码错误.
            - 400: 手机号、密码格式错误.

            """,
        request_body=JsonSchema(
            required=['phone', 'password'],
            properties={
                'phone': StringSchema('手机号码'),
                'password': StringSchema('密码'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDataJsonSchema(data=JsonSchema('UserLoginInformationSerializer')),
            'UserLoginInformationSerializer': AdminLoginSerializers,
        }
    )
    def login(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')
        try:
            # 判断手机号密码是否符合基本条件
            if not judge_phone(phone) or not judge_password_verify(password):
                return Response.code_detail(400, '手机号、密码格式错误')
            # 从数据库查询用户
            user = self.queryset.get(phone=phone, password=pass_en(password))
            # 创建token
            user.token = create_token(user.phone, user.password)
            user.save()
            # 序列化
            user_message = self.get_serializer(user)
            return Response.code_data(200, '成功', Response(user_message.data).data)
        except Administrator.DoesNotExist:
            return Response.code_detail(204, '手机号、密码错误')

    # --------------------------------------------------找回密码--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='找回密码',
        operation_description="""
        **验证码**和**旧密码**需要提供一个 否则400
        ## code
        - 200: 成功.
        - 1003: 未注册.
        - 1004: 原密码错误 或者验证码错误.
        - 400: 参数错误.
        """,
        request_body=JsonSchema(
            required=['phone', 'new_password'],
            properties={
                'phone': StringSchema('手机号码'),
                'code': StringSchema('验证码'),
                'old_password': StringSchema('旧密码'),
                'new_password': StringSchema('新密码'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema()
        }
    )
    def find_back_password(self, request, *args, **kwargs):
        # 获取数据
        phone = request.data.get('phone', '')
        code = request.data.get('code', '')
        old_password = request.data.get('old_password', '')
        new_password = request.data.get('new_password', '')
        try:
            if not judge_phone(phone) or not judge_password_verify(new_password):
                raise UserWarning
            # 判断手机号是否注册
            if Administrator.objects.filter(phone=phone).count() == 0:
                return Response.code_detail(1003, '未注册')
            if judge_msg(phone, code) or Administrator.objects.filter(phone=phone,
                                                                      password=pass_en(old_password)).count() == 1:
                # 修改密码
                self.queryset.filter(phone=phone).update(password=pass_en(new_password))
                return Response.code_detail(200, '密码修改成功')
            else:
                return Response.code_detail(1004, '原密码错误或者验证码错误')
        except UserWarning:
            return Response.code_detail(400, '参数错误')
