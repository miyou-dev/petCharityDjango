import hashlib
import time

from django.core import signing


# 加密
def encrypt(src):
    value = signing.dumps(src)
    value = signing.b64_encode(value.encode()).decode()
    return value


# 生成token信息
def create_token(phone: str, password: str) -> str:
    payload = encrypt({"phone": phone, 'password': password, "time": time.time()})
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(payload.encode())
    signature = md5.hexdigest()
    token = "%s.%s" % (payload, signature)
    return token
