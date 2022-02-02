import os
import sys

from PyQt5.QtCore import pyqtSlot

from crypto import cryptogram_utils
from windows import untitled

from PyQt5.QtWidgets import QApplication, QMainWindow
from amzqr import amzqr


class MyWindow(QMainWindow, untitled.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        # 避免频发更新 设置类的全局变量
        # self._init_event()
        # self.end_Btn.clicked.connect(self.end_event)  # 绑定登陆函数
        # self.pushButton.clicked.connect(self.on_click)
        self._click()

    def _click(self):
        self.pushButton.clicked.connect(self.on_click)

    # @pyqtSlot()
    def on_click(self):
        self.plainTextEdit.setPlainText("hello")


def run():
    version, level, qr_name = amzqr.run(
        "fafaf",
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=None,
        save_dir=os.getcwd()
    )
    return qr_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    app.exec_()
    # name = run()
    # print(name)
