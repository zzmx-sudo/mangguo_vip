import time
from traceback import format_exc

from celery import Celery

from . import settings
from . model import MangoTVModel
from . db_models import ExchangeModel


mobile = None
app = Celery("android.task_process", broker=settings.REDIS_LINK_PATH)

@app.task
def get_sms_code(telephone):
    global mobile
    if mobile is None:
        mobile = MangoTVModel(settings.ANDROID_VERSION)

    while not mobile.isIdle:
        time.sleep(0.2)

    mobile.change_status()
    print("开始获取手机验证码, 手机号: %s" % telephone)
    try:
        mobile.generate_sms_code(telephone)
    except Exception:
        print(f"获取手机验证码失败, 原始报错:\n{format_exc()}")
        mobile = None
        return
    print("获取手机验证码成功, 手机号: %s" % telephone)
    mobile.change_status()

@app.task
def exchange(telephone, sms_code, exchange_code):
    global mobile
    if mobile is None:
        mobile = MangoTVModel(settings.ANDROID_VERSION)

    while not mobile.isIdle:
        time.sleep(0.2)

    mobile.change_status()
    print("开始进行兑换, 手机号: %s" % telephone)
    try:
        result = mobile.login_and_fillIn_redeemCode(telephone, sms_code, exchange_code)
    except Exception as e:
        print(f"兑换失败, 原始报错:\n{format_exc()}")
        ExchangeModel.updateStatus(telephone, sms_code, exchange_code, str(e))
        mobile = None
        return

    ExchangeModel.updateStatus(telephone, sms_code, exchange_code, result)
    print("兑换成功, 手机号: %s" % telephone)
    mobile.change_status()