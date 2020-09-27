from lib.conf.config import settings


class BasePlugin:

    def __init__(self):
        self.DEBUG = settings.DEBUG

    def get_os(self, tgt, fun, arg, handler=None):
        """
        查看目标服务器的系统类型
        :param tgt: 目标主机
        :param fun: 远程执行的salt的模块和方法
        :param arg: 远程执行的salt的模块和方法的参数
        :param handler: 使用的采集数据的方式(默认为saltstack)
        :return:
        """
        result = handler.cmd(tgt, fun, arg)
        system = result.get(tgt, None)
        if system.capitalize() == "Linux":
            return system
        else:
            return "win"

    def process(self, tgt, handler=None):
        """
        根据服务器类型,执行对应的方法,获取资源信息
        :param tgt: 目标主机
        :param handler: 获取资源的方式(默认为saltstack)
        :return:
        """
        if self.get_os(tgt, "cmd.run", ("uname", ), handler=handler) == "win":
            return self.win(tgt, handler=handler)
        else:
            return self.linux(tgt, handler=handler)

    def win(self, tgt, handler=None):
        """通过抛出异常方式实现类的约束,之类必须实现该方法"""
        raise NotImplementedError("win() must be Implemented")

    def linux(self, tgt, handler=None):
        """通过抛出异常方式实现类的约束,之类必须实现该方法"""
        raise NotImplementedError("linux() must be Implemented")