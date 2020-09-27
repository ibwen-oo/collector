import requests
from concurrent.futures import ThreadPoolExecutor

from lib.engine.base import BaseHandler
from lib.utils.saltapi import sapi
from lib.plugins import get_server_info


class SaltHandler(BaseHandler):

    def cmd(self, tgt=None, fun=None, *args):
        """
        远程执行命令的方法
        :param tgt: 目标主机
        :param fun: 在目标主机上执行的方法
        :param args: 方法的参数
        :return:
        """
        result = sapi.process(tgt, fun, *args)
        return result

    def handler(self):
        """
        多线程获取服务器信息,并发送到API模块
        :return:
        """
        pool = ThreadPoolExecutor(5)
        for tgt in self.minions_list:
            pool.submit(self.task, tgt)

    def task(self, tgt):
        server_info = get_server_info(tgt=tgt, handler=self)
        print(server_info)
    #     response =  requests.post(
    #         url=self.cmdbapi,
    #         json=server_info
    #     )
    #
    #     return response




salt = SaltHandler()

