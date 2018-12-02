# 各种响应吗

class RET:
    VALIDATION_DATA = 401  # 无效数据
    ACCEPT = 202 # 已经接受请求，并且已经处理
    FRE_REQUEST = 402 # 请求过于频繁


CODE_MAP = {
    RET.VALIDATION_DATA: "无效的数据",
}

