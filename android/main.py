import sys

from PyQt5.Qt import QApplication, QMainWindow

from main_ui import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("芒果VIP充值服务")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._setup_ui()
        self._setup_event()
        self.show()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid #fb5c12c6;
                border-radius: 5px;
                background-color: rgb(222, 222, 222);
            }}
            {self._open_button_style()}
        """)

    def _setup_event(self):
        self._celery_process = None
        self.ui.handleLogEdit.setReadOnly(True)
        self.ui.powerPushbutton.clicked.connect(lambda : self._power_celery())

    def _power_celery(self):
        if self._celery_process is None:
            # 开启celery进程
            self._celery_process = 1
            self.ui.powerPushbutton.setStyleSheet(f"""
                {self._close_button_style()}
            """)
            self.ui.powerPushbutton.setText("关闭充值服务")
        else:
            # 关闭celery进程
            self._celery_process = None
            self.ui.powerPushbutton.setStyleSheet(f"""
                {self._open_button_style()}
            """)
            self.ui.powerPushbutton.setText("开启充值服务")

    @staticmethod
    def _open_button_style():
        return """
            QPushButton {
                border: 1px solid #fff;
                border-radius: 10px;
                background-color: #fb5c12c6;
                color: #fff;
            }
            QPushButton:hover {
                border: 2px solid #fff;
            }
        """

    @staticmethod
    def _close_button_style():
        return """
            QPushButton {
                border: 1px solid #fb5c12c6;
                border-radius: 10px;
                background-color: rgb(200, 200, 200);
                color: black;
            }
            QPushButton:hover {
                border: 2px solid #fb5c12c6;
            }
        """


if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())