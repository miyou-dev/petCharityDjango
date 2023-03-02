from django.urls import path

from administrator.views.admin_user_view import AdminUserView

urlpatterns = [
    # 登陆
    path('login', AdminUserView.as_view({'post': 'login'})),
    # 找回密码
    path('password/retrieve', AdminUserView.as_view({'patch': 'find_back_password'})),
]
