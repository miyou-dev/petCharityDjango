from django.db.models import F

from user.models import User
from utils.sha1 import pass_en
from utils.validation import judge_phone


# 是否可以注册
def judge_can_register(phone) -> bool:
    return judge_phone(phone) and User.objects.filter(phone=phone).count() == 0


# 判断用户密码是否正确
def judge_password(phone, password) -> bool:
    return User.objects.filter(phone=phone, password=pass_en(password)).count() == 1


# 判断用户支付密码是否正确
def judge_pay_password(phone, pay_password) -> bool:
    return User.objects.filter(phone=phone, pay_password=pass_en(pay_password)).count() == 1


# 支付
def pay(user: User, amount: int) -> bool:
    if user.balance < amount:
        return False
    user.balance = F('balance') - amount
    user.save()
    return True
