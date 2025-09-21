from enum import Enum


class ResultCode(Enum):
    SUCCESS = (200, "操作成功( •̀ ω •́ )✧")
    FAIL = (-1, "操作失败(╬▔皿▔)╯")
    SYSTEM_INNER_ERROR = (500, "系统内部错误╰（‵□′）╯")
    SERVER_UNAVAILABLE = (503, "服务不可用￣へ￣")

    def __init__(self, code, message):
        self.code = code
        self.message = message
