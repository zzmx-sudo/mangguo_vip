import sys
import os

# 项目主路径
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 手机安卓版本
ANDROID_VERSION = "12"

# redis地址和数据库
REDIS_LINK_PATH = "redis://127.0.0.1:6379/8"