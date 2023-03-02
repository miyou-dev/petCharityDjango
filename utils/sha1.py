import hashlib


def pass_en(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest()
