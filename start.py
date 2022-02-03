import os
import sys
import random
import cv2

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic.properties import QtCore
from amzqr import amzqr
from pyqt5_plugins.examplebutton import QtWidgets

from crypto import cryptogram_utils

from windows.QRCodeWindows import QRCodeAESWindow
from windows.qrcodeGenerator import Ui_Dialog

SPLITTER = "+++"


class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        # 避免频发更新 设置类的全局变量
        self.secret_key = cryptogram_utils.gen_secret_key(16)
        self.encrypt_data = ""
        self.total_data = ""
        print("生成密钥信息: ", self.secret_key)
        self._bind_qrcode_generator_button()
        # 图片的一些优化
        self.en_scene = QtWidgets.QGraphicsScene(self)
        self.un_scene = QtWidgets.QGraphicsScene(self)
        self.en_item = ""
        self.un_item = ""

    # 绑定数据类型
    def _bind_data_type(self):
        return

    # 绑定纠错等级
    def _bind_error_level(self):
        return

    # 绑定版本信息
    def _bind_version(self):
        return

    # 绑定二维码大小
    def _bind_qrcode_size(self):
        return

    def _bind_secret_key(self):
        """
        绑定随机密钥
        :return:
        """
        secret_key = cryptogram_utils.gen_secret_key(16)
        self.randomKeyOutput.setPlainText(secret_key)
        self.secret_key = secret_key
        return secret_key

    def _bind_secret_key_ciper(self):
        """
        随机密钥的密文绑定
        :return:
        """
        secret_key = self.secret_key
        ciper_str = cryptogram_utils.aes_encrypt(secret_key, secret_key)
        self.randomKeyCiperOutput.setPlainText(ciper_str)
        self.secret_key = secret_key

    def _bind_sha512(self):
        """
        sha512生成
        :return:
        """
        all_msg = self.ciperAfterOutput.toPlainText()
        print("加密之后的数据: ", all_msg)
        message_digest = cryptogram_utils.sha512(all_msg)
        self.sha512NameOutput.setPlainText(message_digest)
        self.sha512OKOutput.setPlainText("是")
        return message_digest

    def _gen_msg(self):
        """
        所有明文信息生成
        :return:
        """
        # 明文信息
        charge_number = self.deviceNameInput.toPlainText()
        online_time = self.onlineTimeInput.toPlainText()
        device_type = self.deviceTypeInput.toPlainText()
        address = self.addressInput.toPlainText()
        msg = charge_number + SPLITTER + online_time + SPLITTER + device_type + SPLITTER + address
        return msg

    def _gen_ciper_msg(self):
        """
        所有密文信息生成
        :return:
        """
        domain_name = self.seveiceDomainInput.toPlainText()
        token = self.tokenInput.toPlainText()
        expire_time = self.expireTimeInput.toPlainText()
        ciper = domain_name + SPLITTER + token + SPLITTER + expire_time
        print("所有密文信息: ", ciper)
        # ciper_msg = cryptogram_utils.aes_encrypt(self.secret_key, ciper)
        # self.ciperAfterOutput.setPlainText(ciper_msg)
        return ciper

    def _bind_ciper_msg(self):
        """
        密文信息绑定
        :return:
        """
        ciper_msg = self._gen_ciper_msg()
        encrypt_data = cryptogram_utils.aes_encrypt(self.secret_key, ciper_msg)
        self.ciperContentResultOutput.setPlainText(encrypt_data)
        return encrypt_data

    def _bind_ciper_after_msg(self):
        """
        加密之后的数据内容绑定
        :return:
        """
        msg = self._gen_msg()
        ciper_msg = self._gen_ciper_msg()
        all_msg = msg + SPLITTER + ciper_msg
        encrypt_data = cryptogram_utils.aes_encrypt(self.secret_key, all_msg)
        self.total_data = all_msg
        self.encrypt_data = encrypt_data
        self.ciperAfterOutput.setPlainText(encrypt_data)

    def _bind_ciper_before_msg(self):
        """
        加密之前数据内容绑定
        :return:
        """
        msg = self._gen_msg()
        # bjtt-niocloud-charging.nioxyz
        ciper_msg = self._gen_ciper_msg()
        all_msg = msg + SPLITTER + ciper_msg
        self.ciperBeforeOutput.setPlainText(all_msg)

    def show_encrypt_selected_image(self, image_path):
        image = cv2.imread(image_path)
        height = image.shape[0]
        width = image.shape[1]
        ratio = float(height / width)
        new_height = 300
        new_width = int(300 / ratio)
        img = cv2.resize(image, (new_width, new_height))

        frame = QImage(img, new_width, new_height, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.en_item = QGraphicsPixmapItem(pix)
        self.en_scene.addItem(self.en_item)
        self.encrypt_pic.setScene(self.en_scene)

    def show_unencrypt_selected_image(self, image_path):
        image = cv2.imread(image_path)
        height = image.shape[0]
        width = image.shape[1]
        ratio = float(height / width)
        new_height = 300
        new_width = int(300 / ratio)
        img = cv2.resize(image, (new_width, new_height))

        frame = QImage(img, new_width, new_height, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.un_item = QGraphicsPixmapItem(pix)
        self.un_scene.addItem(self.un_item)
        self.unEncrypt_pic.setScene(self.un_scene)

    def utf16to8(self, input_txt: str) -> str:
        """
        转码 解决中文无法转码问题
        :return:
        """
        out = []
        for idx in range(len(input_txt)):
            ch = ord(input_txt[idx])
            if 0x0001 <= ch <= 0x007f:
                out.append(input_txt[idx])
            elif ch > 0x07ff:
                out.append(chr(0xE0 | (ch >> 12 & 0x0F)))
                out.append(chr(0x80 | (ch >> 6 & 0x3F)))
                out.append(chr(0x80 | (ch >> 0 & 0x3F)))
            else:
                out.append(chr(0xC0 | (ch >> 6) & 0x1f))
                out.append(chr(0x80 | (ch >> 0) & 0x3f))

        return ''.join(out)

    def _generate_qrcode(self, encrypt):
        """
        生成qrcode
        :return:
        """
        error_level = self.errorLevelComboBoxInput.currentText()
        size = self.sizeInput.value()

        if not encrypt:
            print("未加密的数据: ", self.total_data)
            version, level, qr_name = amzqr.run(
                self.utf16to8(self.total_data),
                version=1,
                level=error_level,
                picture=None,
                colorized=False,
                contrast=1.0,
                brightness=1.0,
                save_name="un-encrypt.png",
                save_dir=os.getcwd()
            )
            return qr_name
        else:
            print("加密的数据 ", self.encrypt_data)
            version, level, qr_name = amzqr.run(
                self.utf16to8(self.encrypt_data),
                version=1,
                level=error_level,
                picture=None,
                colorized=False,
                contrast=1.0,
                brightness=1.0,
                save_name="encrypt.png",
                save_dir=os.getcwd()
            )
            return qr_name

    def _init_event(self):
        """
        界面输出信息
        说明需要填写的信息填写完成了，需要对输出内容进行绑定
        :return:
        """
        print("触发点击事件:)")
        self._bind_secret_key()
        self._bind_secret_key_ciper()

        self._bind_ciper_msg()
        self._bind_ciper_before_msg()
        self._bind_ciper_after_msg()
        self._bind_secret_key_ciper()
        self._bind_sha512()

        pic_encrypt_path = self._generate_qrcode(True)
        pic_un_encrypt_path = self._generate_qrcode(False)
        self.show_encrypt_selected_image(pic_encrypt_path)
        self.show_unencrypt_selected_image(pic_un_encrypt_path)

    def _bind_qrcode_generator_button(self):
        """
        生成二维码信息按钮
        :return:
        """
        self.qrcodeGenButton.clicked.connect(self._init_event)


def run():
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    app.exec_()


if __name__ == '__main__':
    run()
