import random
import re
import cProfile
from hashlib import md5

"""
param: len int
return : str(int)
"""
def random_sms(len):
    if len <=0:
        raise("Invalid param 'len'!")
    return str(random.randint(10**(len-1), 10**len))

# 检查密码是否合法
# 复杂度：
# 1.长度 8-32
# 2.包含大写字符
# 3.包含小写字符
# 4.包含特殊字符
def check_upper(password):
    rex = "[A-Z]+"
    pattern = re.compile(rex)
    return pattern.search(password)


def check_lower(password):
    rex = "[a-z]+"
    pattern = re.compile(rex)
    return pattern.search(password)


def check_special(password):
    rex = "[\!\#\$%\&\*]"
    pattern = re.compile(rex)
    return pattern.search(password)


def check_password(password):
    if check_upper(password) and check_lower(password) and check_special(password):
        return True
    return False


# hash字符串
# return string
def hash_str(str, salt):
    return md5((str+salt).encode("utf-8")).hexdigest()


