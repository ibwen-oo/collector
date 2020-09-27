import os
import sys

# 自定义配置文件路径
os.environ["USER_SETTING"] = 'config.settings'

# 项目目录加入sys.path中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
