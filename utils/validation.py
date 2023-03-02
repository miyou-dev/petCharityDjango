import re


# 判断手机号是否合法
def judge_phone(phone: str) -> bool:
    return re.match(r'^1[345678]\d{9}$', phone) is not None


# 判断密码是否合法
def judge_password_verify(password: str) -> bool:
    if password is None:
        return False

    return re.match(r'[a-zA-Z0-9._]{8,20}', password) is not None


# 判断支付密码是否合法
def judge_pay_password_verify(password: str) -> bool:
    if password is None:
        return False

    return re.match(r'[0-9]{6}', password) is not None


# 真名验证
def judge_real_name_verify(real_name: str) -> bool:
    return real_name is not None and len(real_name.strip()) >= 2


# 判断身份证是否合法
def judge_id_card_verify(id_card: str) -> bool:
    if id_card is None or len(id_card) != 18:
        return False

    factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_sum = sum([x * y for x, y in zip(factor, [int(a) for a in id_card[0:-1]])])
    return ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'][check_sum % 11] == id_card[-1]


# 昵称验证
def judge_nickname_verify(nickname: str) -> bool:
    return nickname is not None and len(nickname.strip()) >= 1
