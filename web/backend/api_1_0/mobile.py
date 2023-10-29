import re
from . import api
from flask import jsonify, request


@api.route("/get_sms", methods=["POST"])
def get_login_mobile():
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

    #  TODO 调用接口函数，传入手机号发送手机验证码

    return jsonify(errno="200", errmsg="手机号格式正确")


@api.route("/exchange", methods=["POST"])
def get_login_code():
    # 获取手机验证码，兑换码
    req_dict = request.get_json()
    if not req_dict:
        return jsonify(errno="201", errmsg="参数不完整")

    mobile = req_dict.get("telephone")
    sms_code = req_dict.get("sms_code")
    exchange_code = req_dict.get("exchange_code")
    if not all([mobile, sms_code, exchange_code]):
        return jsonify(errno="201", errmsg="参数不完整")

    #  TODO  调用接口函数，传入验证码，验证是否登入成功，登陆成功后验证是否兑换成功

    return jsonify(errno="200", errmsg="兑换成功")



