"""
Django settings for petCharity project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7pzv#(c9@*q!#_!^qw%a)6*-$pjn6xezo+jir9-d56iqff-l-%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'corsheaders',  # 跨域
    'address.apps.AddressConfig',  # 地址
    'user.apps.UserConfig',  # 用户
    'administrator.apps.AdministratorConfig',  # 管理员
    'pet.apps.PetConfig',  # 宠物
    'donate.apps.DonateConfig',  # 宠物帮助众筹
    'adopt.apps.AdoptConfig',  # 宠物领养
    # 'pet_public_server.apps.PetPublicServerConfig',  # 宠物公有接口
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'petCharity.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'petCharity.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 设置静态文件路径为主目录下的picture文件夹
MEDIA_ROOT = os.path.join(BASE_DIR, 'file').replace('\\', '/')
# url映射
MEDIA_URL = '/statics/'

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
# 允许所有来源访问
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'utils-agent',
    'x-csrftoken',
    'x-requested-with',
    'token'
)

REST_FRAMEWORK = {
    # 身份验证类
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'utils.authentication.UserAuthentication',
    ),
    # 指定默认schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 默认分页
    'DEFAULT_PAGINATION_CLASS': 'utils.paginations.myPageNumberPagination.MyPageNumberPagination',
    # 支持解释器 json and form
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser'],
    # 频率控制
    'DEFAULT_THROTTLE_RATES': {
        # 发送验证码频率
        'SendVerificationFrequency': '10/m',
    },
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

}
# 设置为指向该路由对象作为您的根应用程序
ASGI_APPLICATION = 'PetCharityPlatform.routing.application'

# simpleui 设置
SIMPLEUI_DEFAULT_THEME = 'dark.green.css'
# SIMPLEUI_DEFAULT_THEME = 'black.css'
# SIMPLEUI_DEFAULT_THEME = 'e-purple-pro.css'

SIMPLEUI_LOGO = '/statics/user/head/head.png'
# 服务器信息
SIMPLEUI_HOME_INFO = False
# 使用分析
SIMPLEUI_ANALYSIS = False
SIMPLEUI_ICON = {
    '用户': 'fa-solid fa-user',
    '用户关注': 'fa-solid fa-shield-heart',
    '用户收藏': 'fa-solid fa-heart',

    '管理员用户': 'fa-sharp fa-solid fa-hammer',

    '宠物': 'fa-solid fa-paw',
    '宠物品种': 'fa-sharp fa-solid fa-shield-cat',
    '宠物图片': 'fa-solid fa-image',
    '宠物图片映射': 'fa-solid fa-bars',

    '宠物帮助众筹': 'fa-solid fa-hand-holding-medical',
    '宠物帮助众筹图片映射': 'fa-solid fa-bars',
    '宠物帮助众筹捐赠名单': 'fa-solid fa-list',

    '联系方式': 'fa-solid fa-address-card',
    '宠物领养': 'fa-solid fa-handshake-angle',
    '宠物领养交易订单': 'fa-solid fa-list',
}
