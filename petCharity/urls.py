from django.urls import path, re_path, include

from rest_framework.permissions import AllowAny
from drf_yasg.openapi import Info, Contact, License
from drf_yasg.views import get_schema_view

from django.contrib import admin

from django.views.generic import RedirectView
from django.conf.urls.static import static

from petCharity import settings

schema_view = get_schema_view(
    Info(
        title="宠物爱心公益平台 API",
        default_version='v2',
        description="接口文档",
        terms_of_service="#",
        contact=Contact(email="2254235902@qq.com"),
        license=License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('', RedirectView.as_view(url='swagger')),
    # drf-yasg 配置
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    # 地址
    path('address/', include('address.urls')),
    # 用户
    path('user/', include('user.urls')),
    # 管理员用户
    path('administrator/', include('administrator.urls')),
    # 宠物
    path('pet/', include('pet.urls')),
    # 宠物帮助众筹宠物
    path('donate/', include('donate.urls')),
    # 宠物领养
    path('adopt/', include('adopt.urls')),
    # 问答
    path('ask/', include('question.urls')),

    path('statistics/', include('other.urls')),
]

# 访问静态资源
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
