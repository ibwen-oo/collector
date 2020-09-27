import os
import logging
from lib.conf.config import settings


class Log:
    """记录日志"""
    def __init__(self, filename, level):
        logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d-%H:%M:%S")
        self.logger = logging.getLogger(__name__)
        # 设置日志级别
        self.logger.setLevel(level)
        # 日志文件地址
        log_file = logging.FileHandler(filename, encoding="utf-8")
        # 设置日志格式
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s: %(message)s")
        log_file.setFormatter(formatter)
        # logger 对象添加 handler
        self.logger.addHandler(log_file)

# 记录 cmdb 日志, 单例对象
cmdb_log = Log(os.path.join(settings.LOG_FILE_PATH, settings.LOG_NAME), logging.DEBUG)

# print(os.path.join(settings.LOG_FILE_PATH, settings.LOG_NAME))

# 如果还有别的类型的日志需要记录，再创建一个单例对象即可
# other_log = Log("/log/path/other.log", level)