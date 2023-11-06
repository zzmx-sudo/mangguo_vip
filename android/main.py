import sys
import subprocess
import time
from datetime import datetime

import psutil
from PyQt5.Qt import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal

from main_ui import Ui_MainWindow
import settings

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
            self._start_celery()
            self.ui.powerPushbutton.setStyleSheet(f"""
                {self._close_button_style()}
            """)
            self.ui.powerPushbutton.setText("关闭充值服务")
        else:
            # 关闭celery进程
            self._close_celery()

    def _start_celery(self):
        cwd = settings.BASE_DIR
        cmd = "celery -A android.task_process worker -l info -c 1"
        self._celery_process = subprocess.Popen(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        self._watch_thread = WatchCeleryThread(self._celery_process)
        self._watch_thread.signal.connect(self._watch_celery_status)
        self._watch_thread.start()
        self.ui.handleLogEdit.append(self._add_datetime_to_msg("充值服务已开启"))

    def _close_celery(self):
        self._kill_process(self._celery_process.pid)
        self.ui.handleLogEdit.append(self._add_datetime_to_msg("充值服务已关闭"))
        self._watch_thread.run_flag = False
        self._watch_thread.quit()
        self._celery_process = None
        self.ui.powerPushbutton.setStyleSheet(f"""
            {self._open_button_style()}
        """)
        self.ui.powerPushbutton.setText("开启充值服务")

    def _watch_celery_status(self, status):
        flag, msg = status
        if flag == "doing":
            self.ui.handleLogEdit.append(self._add_datetime_to_msg(msg))
        elif flag == "exit":
            if msg == 0:
                self.ui.handleLogEdit.append(self._add_datetime_to_msg("充值服务正常退出"))
            else:
                self.ui.handleLogEdit.append(self._add_datetime_to_msg("充值服务异常退出"))
                self._close_celery()

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

    def _kill_process(self, pid):
        try:
            process = psutil.Process(pid)
        except:
            return

        for child in process.children(recursive=True):
            child.kill()

        process.kill()

    def _add_datetime_to_msg(self, origin_msg):
        return "[%s] - %s" % (
            datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), origin_msg
        )


class WatchCeleryThread(QThread):
    signal = pyqtSignal(tuple)

    def __init__(self, process):
        super(WatchCeleryThread, self).__init__()
        self._process: subprocess.Popen = process
        self.run_flag = True

    def run(self):
        while self.run_flag:
            if self._process.poll() is not None:
                self.signal.emit(("exit", self._process.poll()))
                continue

            line = self._process.stdout.readline().strip().decode("utf-8", errors="ignore")
            while line:
                self.signal.emit(("doing", line))
                line = self._process.stdout.readline().strip().decode("utf-8", errors="ignore")

            time.sleep(3)


if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())