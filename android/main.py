import sys

from PyQt5.Qt import QApplication, QMainWindow

class MainWindow(QMainWindow):

    pass


if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())