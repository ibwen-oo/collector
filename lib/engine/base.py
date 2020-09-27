from lib.utils import saltapi
from lib.conf.config import settings


class BaseHandler():
    """约束基类"""

    def __init__(self):
        # 获取被salt管理的服务器列表
        self.minions_list, _ = saltapi.sapi.list_all_key()
        # 定义api模块的url地址
        self.cmdbapi = settings.CMDBAPI

    def cmd(self, hostname, command):
        raise NotImplementedError("cmd() must be Implemented")

    def handler(self):
        raise NotImplementedError("handler() must be Implemented")

