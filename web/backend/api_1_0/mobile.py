import re

from flask import jsonify, request

from . import api
from android.task_process import get_sms_code, exchange


@api.route("/get_sms", methods=["POST"])
def get_sms():
    # 获取手机号
    req_dict = request.get_json()
    if not req_dict or not req_dict.get("telephone"):
        return jsonify(errno="201", errmsg="参数不完整")

    mobile = req_dict.get("telephone")
    # 校验参数
    # 手机号的格式
    if not re.match(r"1[345678]\d{9}", mobile):
        # 表示格式不对
        return jsonify(errno="201", errmsg="手机号格式错误")

    get_sms_code.delay(mobile)

    return jsonify(errno="200", errmsg="手机号格式正确")


@api.route("/exchange", methods=["POST"])
def exchange():
    # 获取手机验证码，兑换码
    req_dict = request.get_json()
    if not req_dict:
        return jsonify(errno="201", errmsg="参数不完整")

    mobile = req_dict.get("telephone")
    sms_code = req_dict.get("sms_code")
    exchange_code = req_dict.get("exchange_code")
    if not all([mobile, sms_code, exchange_code]):
        return jsonify(errno="201", errmsg="参数不完整")

    if len(sms_code) != 6 or len(exchange_code) != 8:
        return jsonify(errno="201", errmsg="验证码或兑换码不正确")

    # TODO: 若兑换码曾兑换成功, 不让其反复兑换

    exchange.delay(mobile, sms_code, exchange_code)

    return jsonify(errno="200", errmsg="兑换成功")
