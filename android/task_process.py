import time

from celery import Celery

import settings
from . model import MangoTVModel


mobile = None
app = Celery("task_process", broker=settings.REDIS_LINK_PATH)

@app.task
def get_sms_code(telephone):
    global mobile
    if mobile is None:
        mobile = MangoTVModel(settings.ANDROID_VERSION)

    while not mobile.isIdle:
        time.sleep(0.2)

    mobile.change_status()
    mobile.generate_sms_code(telephone)
    mobile.change_status()

@app.task
def exchange(telephone, sms_code, exchange_code):
    global mobile
    if mobile is None:
        mobile = MangoTVModel(settings.ANDROID_VERSION)

    while not mobile.isIdle:
        time.sleep(0.2)

    mobile.change_status()
    result = mobile.login_and_fillIn_redeemCode(telephone, sms_code, exchange_code)
    # TODO: 修改数据库状态
    mobile.change_status()