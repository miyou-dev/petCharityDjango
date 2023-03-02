from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

# 用户工具
from user.utils.tools import judge_can_register, judge_pay_password, judge_password
# 数据验证
from utils.validation import judge_phone, judge_password_verify, judge_pay_password_verify
# token
from utils.token import create_token
# 验证码功能
from utils.msg import judge_msg, MSG_ERROR
# 密码加密
from utils.sha1 import pass_en

# 序列化
from user.utils.serializers import UserLoginInformationSerializer, UserPublicInformationSerializer
# 模型
from user.models import User
# 接口文档简写
from utils.api.schema import JsonSchema, StringSchema, CodeDetailSchema, WhetherDetailSchema, CodeDataJsonSchema
# 添加功能的 Response
from utils.response.response import Response


class UserView(RetrieveModelMixin, GenericViewSet):
    """
    retrieve:
      获取用户公开信息

      需要ID 否则404

    """
    authentication_classes = []
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginInformationSerializer
        return UserPublicInformationSerializer

    # --------------------------------------------------登录--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='登录',
        operation_description="""
        ## 返回用户信息
        ### code
        - 200: 成功.
        - 204: 手机号、密码、验证码错误.
        - 400: 手机号格式错误.
        
        """,
        request_body=JsonSchema(
            required=['phone'],
            properties={
                'phone': StringSchema('手机号码'),
                'password': StringSchema('密码'),
                'code': StringSchema('验证码')
            },
        ),
        responses={
            HTTP_200_OK: CodeDataJsonSchema(data=JsonSchema('UserLoginInformationSerializer')),
            'UserLoginInformationSerializer': UserLoginInformationSerializer,
        }
    )
    def login(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')
        code = request.data.get('code', '')
        try:
            # 判断手机号密码是否符合基本条件
            if not judge_phone(phone):
                return Response.code_detail(400, '手机号格式错误')
            if judge_msg(phone, code):
                # 验证码登录
                user = self.queryset.get(phone=phone)
            else:
                # 从数据库查询用户
                user = self.queryset.get(phone=phone, password=pass_en(password))
            # 创建token
            user.token = create_token(user.phone, user.password)
            user.save()
            # 序列化
            user_message = self.get_serializer(user)
            return Response.code_data(200, '成功', Response(user_message.data).data)
        except User.DoesNotExist:
            return Response.code_detail(204, '手机号、密码、验证码错误')

    # --------------------------------------------------注册--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='注册',
        operation_description="""
        ## code
        - 1001: 验证码错误.
        - 1002: 用户已存在.
        - 400: 手机号码非法.
        """,
        request_body=JsonSchema(
            required=['phone', 'code'],
            properties={
                'phone': StringSchema('手机号码'),
                'code': StringSchema('验证码'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema(),
        }
    )
    def create(self, request, *args, **kwargs):
        # 获取数据
        phone = request.data.get('phone', '')
        # 验证数据基本要求
        if not judge_phone(phone):
            return Response.code_detail(400, f'手机号码非法')
        # 判断验证码是否正确
        if not judge_msg(phone, request.data.get('code', '')):
            # 验证码错误
            return Response.code_detail(1001, MSG_ERROR)
        # 是否已注册
        if not judge_can_register(phone):
            return Response.code_detail(1002, '手机号已注册')
        # 新建用户
        user = self.queryset.create(phone=phone)
        print(f'注册 {user.phone}')
        return Response.code_detail(200, '注册成功')

    # --------------------------------------------------找回密码--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='找回密码',
        operation_description="""
        **验证码**和**旧密码**需要提供一个 否则400
        ## code
        - 200: 成功.
        - 1003: 用户未注册.
        - 1004: 原密码错误 或者验证码错误.
        - 400: 参数错误.
        """,
        request_body=JsonSchema(
            required=['phone', 'newPassword'],
            properties={
                'phone': StringSchema('手机号码'),
                'code': StringSchema('验证码'),
                'oldPassword': StringSchema('旧密码'),
                'newPassword': StringSchema('新密码'),
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
        old_password = request.data.get('oldPassword', '')
        new_password = request.data.get('newPassword', '')
        try:
            if not judge_phone(phone) or not judge_password_verify(new_password):
                raise UserWarning
            # 判断手机号是否注册
            if judge_can_register(phone):
                return Response.code_detail(1003, '用户未注册')
            if judge_msg(phone, code) or judge_password(phone, old_password):
                # 修改密码
                self.queryset.filter(phone=phone).update(password=pass_en(new_password))
                return Response.code_detail(200, '密码修改成功')
            else:
                return Response.code_detail(1004, '原密码错误或者验证码错误')
        except UserWarning:
            return Response.code_detail(400, '参数错误')

    #   --------------------------------------------------找回支付密码--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='找回支付密码',
        operation_description="""
        **验证码**和**旧密码**需要提供一个 否则400
        ## code
        - 200: 成功.
        - 1004: 原密码错误 或者验证码错误.
        - 400: 参数错误.
        """,
        request_body=JsonSchema(
            required=['phone', 'newPayPassword'],
            properties={
                'phone': StringSchema('手机号码'),
                'code': StringSchema('验证码'),
                'oldPayPassword': StringSchema('旧支付密码'),
                'newPayPassword': StringSchema('新支付密码'),
            },
        ),
        responses={
            HTTP_200_OK: CodeDetailSchema()
        }
    )
    def find_back_pay_password(self, request, *args, **kwargs):
        # 获取数据
        phone = request.data.get('phone', '')
        code = request.data.get('code', '')
        old_pay_password = request.data.get('oldPayPassword', '')
        new_pay_password = request.data.get('newPayPassword', '')
        try:
            if not judge_phone(phone) or not judge_pay_password_verify(new_pay_password):
                raise UserWarning
            if judge_msg(phone, code) or judge_pay_password(phone, old_pay_password):
                # 修改密码
                self.queryset.filter(phone=phone).update(pay_password=pass_en(new_pay_password))
                return Response.code_detail(200, '支付密码修改成功')
            else:
                return Response.code_detail(1004, '原支付密码错误或者验证码错误')
        except UserWarning:
            return Response.code_detail(400, '参数错误')

    # --------------------------------------------------判断用户是否注册--------------------------------------------------
    @swagger_auto_schema(
        operation_summary='判断用户是否注册',
        operation_description='True 未注册（可以注册）',
        request_body=JsonSchema(
            required=['phone'],
            properties={'phone': StringSchema('用户名（手机号码）')},
        ),
        responses={
            HTTP_200_OK: WhetherDetailSchema('是否注册'),
        }
    )
    def judge_phone_registered(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        try:
            if not judge_phone(phone):
                raise UserWarning
            whether = judge_can_register(phone)
            detail = '手机号未注册' if whether else '手机号已注册'
            return Response.whether_detail(200, whether, detail)
        except UserWarning:
            pass
        return Response.code_detail(400, '参数错误')
