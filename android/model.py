import socket
from appium import webdriver
from appium.webdriver.extensions.android.nativekey import AndroidKey

class MangoTVModel:

    def __init__(self, android_version):

        self._android_version = android_version
        err_init_msg = self._check_env()
        if err_init_msg:
            raise SystemError(f"环境校验不通过, 初始化模块失败, 环境校验信息: {err_init_msg}")

        self._driver = None
        self._setup()

    def generate_sms_code(self, phone_number):
        """
        填入手机号并点击获取验证码
        """

    def login_and_fillIn_redeemCode(self, phone_number, smsCode, redeemCode):
        """
        登录并填入兑换码兑换
        """

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

        return ""

    def _setup(self):
        """
        连接手机并打开芒果TV APP，若登录退出登录
        """
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': self._android_version,
            'deviceName': 'xxx',
            'appPackage': 'tv.danmaku.bili',
            'appActivity': '.ui.splash.SplashActivity',
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

        # TODO: 点击个人信息页面  若登录退出
        # 若有跳过按钮则点击

    def _check_back_profile(self):
        """
        校验APP已经退出账号并在个人页面
        """