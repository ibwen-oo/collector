import importlib

# 单例模式,导入settings对象
from lib.conf.config import settings


def run():
    engine_path = settings.ENGINE_DICT.get(settings.ENGINE)
    model_str, cls_str = engine_path.rsplit(".", maxsplit=1)
    model = importlib.import_module(model_str)
    cls = getattr(model, cls_str)
    obj = cls()
    obj.handler()

if __name__ == "__main__":
    run()