import os
import importlib

from lib.conf import global_settings

class Settings:
    """初始化配置文件,把配置文件中的配置项初始化成Settings类的属性"""
    def __init__(self):
        # 获取默认配置
        # 循环global_settings中的属性
        for name in dir(global_settings):
            if name.isupper():
                val = getattr(global_settings, name)
                setattr(self, name, val)

        # 获取用户自定义配置
        # 循环用户自定义配置文件中的的属性
        model_path = os.environ.get("USER_SETTING")
        model = importlib.import_module(model_path)
        for name in dir(model):
            if name.isupper():
                val = getattr(model, name)
                setattr(self, name, val)

settings = Settings()
