from django.core.cache import cache

CODE_TIME_OUT = 300  # 5min


# 发送验证码
def send_msg(phone: str) -> bool:
    cache.set(f'{phone}_code', phone[-4:], CODE_TIME_OUT)  # 存储到缓存中
    return True


# 判断验证码
def judge_msg(phone: str, code: str) -> bool:
    if code is None:
        return False
    return cache.get(f'{phone}_code') == code


MSG_ERROR = '验证码错误'
