import re
import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow


def is_integer(text):
    return re.fullmatch(r"-?\d+", text) is not None


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_Decrypt.clicked.connect(self.call_api_decrypt)

    def show_message(self, icon, title, text):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def call_api_encrypt(self):
        plain_text = self.ui.txt_PlainText.toPlainText()
        key_input = self.ui.txt_Key.text()

        if not plain_text.strip():
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "PlainText của RailFence không được để trống nha.",
            )
            return

        if not is_integer(key_input):
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence phải là số nguyên nha.",
            )
            return
        key = int(key_input)

        if key < 2:
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence phải lớn hơn hoặc bằng 2 nha.",
            )
            return

        if key > len(plain_text):
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence không được lớn hơn độ dài PlainText nha.",
            )
            return

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key,
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_CipherText.setText(data["encrypted_text"])
                self.show_message(QMessageBox.Information, "Thành công", "Encrypted Successfully")
            else:
                self.show_message(QMessageBox.Critical, "Lỗi API", f"Server trả về lỗi nội bộ (Status code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            self.show_message(QMessageBox.Critical, "Lỗi kết nối", f"Không thể kết nối đến Server API!\nChi tiết: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_CipherText.toPlainText()
        key_input = self.ui.txt_Key.text()

        if not cipher_text.strip():
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "CipherText của RailFence không được để trống nha.",
            )
            return

        if not is_integer(key_input):
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence phải là số nguyên nha.",
            )
            return
        key = int(key_input)

        if key < 2:
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence phải lớn hơn hoặc bằng 2 nha.",
            )
            return

        if key > len(cipher_text):
            self.show_message(
                QMessageBox.Warning,
                "Lỗi nhập liệu",
                "Key của RailFence không được lớn hơn độ dài CipherText nha.",
            )
            return

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key,
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_PlainText.setText(data["decrypted_text"])
                self.show_message(QMessageBox.Information, "Thành công", "Decrypted Successfully")
            else:
                self.show_message(QMessageBox.Critical, "Lỗi API", f"Server trả về lỗi nội bộ (Status code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            self.show_message(QMessageBox.Critical, "Lỗi kết nối", f"Không thể kết nối đến Server API!\nChi tiết: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
