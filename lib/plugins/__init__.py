import importlib
from lib.conf.config import settings


def get_server_info(tgt=None, handler=None):
    """
    遍历PLUGINS_DICT,获取自定义的服务器信息
    :param tgt: 目标服务器
    :param handler: 所选engine的handler方法
    :return:
    """
    server_info = {}
    for name, path in settings.PLUGINS_DICT.items():
        # print("PLUGIN: ", name, path)
        model_str, cls_str = path.rsplit(".", maxsplit=1)
        # print(cls_str, model_str)
        model = importlib.import_module(model_str)
        # print("model: ", model)
        cls = getattr(model, cls_str)
        obj = cls()
        value = obj.process(tgt, handler=handler)
        server_info[name] = value

    return server_info


def get_host_info():
    result = []
    for key, path in settings.HostCOLLECTOR_CLASS_DICT.items():
        model_path, model_class = path.rsplit(".", 1)
        # print(model_path, model_class)
        model = importlib.import_module(model_path)
        cls = getattr(model, model_class)
        ins = cls(host=settings.vCenter["host"], user=settings.vCenter["user"], password=settings.vCenter["password"])
        data = ins.process()
        result.append(data)
    return result

def get_vm_info(name):
    result = []

    for key, path in settings.VMCOLLECTOR_CLASS_DICT.items():
        model_path, model_class = path.rsplit(".", 1)
        # print(model_path, model_class)
        model = importlib.import_module(model_path)
        cls = getattr(model, model_class)
        ins = cls(host=settings.vCenter["host"], user=settings.vCenter["user"], password=settings.vCenter["password"])
        data = ins.process(name)
        result.append(data)

    return result