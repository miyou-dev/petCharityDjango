from django.urls import path, include

from user.views.contact_view import ContactView
from user.views.send_vcode_view import SendVCodeView
from user.views.user_feedback_view import UserFeedbackView, AdminUserFeedbackView
from user.views.user_image_view import UserImageView
from user.views.user_collect_view import UserCollectView
from user.views.user_following_view import UserFollowingView
from user.views.user_token_view import UserTokenView
from user.views.user_view import UserView

urlpatterns = [
    # 发送验证码
    path('sendVCode', SendVCodeView.as_view()),

    # --------------------------------------------------用户登录注册...--------------------------------------------------
    # 登录
    path('login', UserView.as_view({'post': 'login'})),
    # 注册
    path('register', UserView.as_view({'post': 'create'})),
    # 获取用户公共信息
    path('information/get/<int:pk>', UserView.as_view({'get': 'retrieve'})),
    # 找回密码
    path('password/retrieve', UserView.as_view({'patch': 'find_back_password'})),
    # 找回支付密码
    path('password/pay/retrieve', UserView.as_view({'patch': 'find_back_pay_password'})),
    # 判断手机号是否注册
    path('whetherRegister', UserView.as_view({'post': 'judge_phone_registered'})),
    # 用户联系方式修改
    path('contact', ContactView.as_view()),

    # --------------------------------------------------用户登录后--------------------------------------------------
    # 收藏
    path('collect', UserCollectView.as_view()),

    # Token获取用户信息 修改用户信息
    path('token/information', UserTokenView.as_view({'post': 'information', 'patch': 'partial_update'})),
    # 实名认证
    path('authentication', UserTokenView.as_view({'post': 'authentication'})),

    # --------------------------------------------------用户关注--------------------------------------------------
    path('followers/', include([
        # 获取用户关注用户信息
        path('list', UserFollowingView.as_view({'get': 'list'})),
        # 关注/取消关注用户
        path('user', UserFollowingView.as_view({'post': 'post'})),
    ])),

    # --------------------------------------------------头像上传--------------------------------------------------
    path('avatar/upload', UserImageView.as_view({'post': 'partial_update'})),

    # --------------------------------------------------用户反馈--------------------------------------------------
    path('feedback', UserFeedbackView.as_view({'post': 'create'})),
    path('feedback/list', AdminUserFeedbackView.as_view({'get': 'list'})),
    path('feedback/<int:pk>', AdminUserFeedbackView.as_view({'delete': 'destroy'})),
]
