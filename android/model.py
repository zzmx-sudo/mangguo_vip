import os
import time
import socket
from typing import Union
from threading import RLock

from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.common import exceptions as s_exceptions


class MangoTVModel:

    def __init__(self, android_version):

        self._android_version = android_version
        err_init_msg = self._check_env()
        if err_init_msg:
            raise SystemError(f"环境校验不通过, 初始化模块失败, 环境校验信息: {err_init_msg}")

        self._driver: Union[webdriver.Remote, None] = None
        self._window_width = 0
        self._window_height = 0
        self._is_idle = False
        self._lock = RLock()
        self._setup()
        self.change_status()

    def generate_sms_code(self, phone_number):
        """
        填入手机号并点击获取验证码
        """
        self._check_back_profile()
        self._driver.find_element_by_id("tvNickname").click()
        elements = self._driver.find_elements_by_id("tvText")
        if elements:
            for element in elements:
                if element.text == "切换账号":
                    element.click()
                    break

        phone_clear = self._driver.find_element_by_id("ivClear")
        if phone_clear: phone_clear.click()

        elements = self._driver.find_elements_by_id("etContent")
        if elements:
            for element in elements:
                if element.text == "请输入手机号":
                    element.click()
                    element.send_keys(phone_number)
                    break
        self._driver.find_element_by_id("checkBox").click()
        self._driver.find_element_by_id("tvCheck").click()
        self._driver.find_element_by_id("ivRight").click()

        return ""

    def login_and_fillIn_redeemCode(self, phone_number, smsCode, redeemCode):
        """
        登录并填入兑换码兑换
        """
        self._check_back_profile()
        self._driver.find_element_by_id("tvNickname").click()
        elements = self._driver.find_elements_by_id("tvText")
        if elements:
            for element in elements:
                if element.text == "切换账号":
                    element.click()
                    break

        phone_clear = self._driver.find_element_by_id("ivClear")
        if phone_clear: phone_clear.click()

        elements = self._driver.find_elements_by_id("etContent")
        input_phone, input_sms = False, False
        if elements:
            for element in elements:
                if element.text == "请输入手机号":
                    element.click()
                    element.send_keys(phone_number)
                    input_phone = True
                    if input_sms: break
                elif element.text == "请输入校验码":
                    element.click()
                    element.send_keys(smsCode)
                    input_sms = True
                    if input_phone: break
        if not input_phone or not input_sms:
            return "登录失败, 未能正确输入手机号和验证码"
        self._driver.find_element_by_id("checkBox").click()
        self._driver.find_element_by_id("tvText").click()
        try:
            close_button = self._driver.find_element_by_id("ivRight")
        except s_exceptions.NoSuchElementException:
            pass
        else:
            close_button.click()
            return "登录失败, 验证码不正确或失效"
        # TODO: 兑换操作
        return "SUCC"

    def quit(self):
        """
        定义退出操作
        """
        if self._driver is not None:
            self._driver.quit()

    def _check_env(self):
        """
        参数校验
        """
        try:
            int(self._android_version)
        except Exception as e:
            return f"输入的安卓版本不合法, 原始错误: {e}"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect(("127.0.0.1", 4723))
        except Exception:
            return "未检测到开启的AppIum, 请以4723端口开启AppIum后再运行程序"
        finally:
            sock.close()

        devices = os.popen("adb devices").read().replace("List of devices attached", "").strip()
        if not devices:
            return "未检测到USB调试设备, 请手机打开USB调试后连接电脑在运行程序"

        return ""

    def _setup(self):
        """
        连接手机并打开芒果TV APP，若登录退出登录
        """
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': self._android_version,
            'deviceName': 'xxx',
            'appPackage': 'com.hunantv.imgo.activity',
            'appActivity': '.MainActivity',
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'noReset': True,
            'newCommandTimeout': 6000,
            'automationName': 'UiAutomator2'
        }
        try:
            self._driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        except Exception as e:
            raise SystemError(f"尝试连接手机异常, 原始错误: {e}")

        self._window_width = self._driver.get_window_size()["width"]
        self._window_height = self._driver.get_window_size()["height"]
        # 配置缺省等待正常打开APP的时间
        self._driver.implicitly_wait(10)

        # 进入APP后确认是退出登录状态
        self._check_back_profile()

    def _check_back_profile(self):
        """
        校验APP已经退出账号并在我的页面, 若不是进入该状态
        """
        try:
            bottom_menus = self._driver.find_elements_by_id("viewTabPlaceholder")
        except s_exceptions.NoSuchElementException:
            return False

        # 进入我的页面
        bottom_menus[-1].click()

        # 获取用户名, 若用户名不为立即登录则表示已经登录, 需退出登录
        username = self._driver.find_element_by_id("tvNickname")
        if username.text != "立即登录":
            self._logout()

    def _logout(self):
        """
        退出用户登录
        :return: bool -> 是否成功退出登录
        """
        setting = self._driver.find_element_by_id("setting")
        if not setting:
            return False
        setting.click()

        while True:
            self._driver.swipe(
                int(self._window_width*0.5), int(self._window_height*0.9),
                int(self._window_width*0.5), int(self._window_height*0.1),
                1000
            )
            elements = self._driver.find_elements_by_id("tvTitle")
            if elements and elements[-1].text == "退出登录":
                break

        self._driver.find_elements_by_id("tvTitle")[-1].click()
        return True

    def change_status(self):
        """
        修改空闲状态
        """
        with self._lock:
            self._is_idle = not self._is_idle

    @property
    def isIdle(self):

        return self._is_idle


if __name__ == '__main__':
    obj = MangoTVModel("12")
    # obj.generate_sms_code("123456")
    result = obj.login_and_fillIn_redeemCode("123456", "370048", "Xad")
    print(result)
    obj.quit()