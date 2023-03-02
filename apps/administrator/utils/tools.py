from utils.sha1 import pass_en
from utils.validation import judge_phone

from administrator.models import Administrator


# 是否可以注册
def judge_can_register(phone) -> bool:
    return judge_phone(phone) and Administrator.objects.filter(phone=phone).count() == 0


# 判断用户密码是否正确
def judge_password(phone, password) -> bool:
    return Administrator.objects.filter(phone=phone, password=pass_en(password)).count() == 1
