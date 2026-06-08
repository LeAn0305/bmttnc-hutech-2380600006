import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_Decrypt.clicked.connect(self.call_api_decrypt)

    def show_message(self, icon, title, text):
        """Hàm tiện ích hiển thị nhanh pop-up thông báo"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def call_api_encrypt(self):
        # Lấy dữ liệu và xóa khoảng trắng thừa
        plain_text = self.ui.txt_PlainText.toPlainText().strip()
        key_input = self.ui.txt_Key.text().strip()

        # ================= RÀNG BUỘC ĐẦU VÀO (VALIDATION) =================
        if not plain_text:
            self.show_message(QMessageBox.Warning, "Lỗi nhập liệu", "Vui lòng nhập văn bản cần mã hóa (Plain Text)!")
            return

        if not key_input:
            self.show_message(QMessageBox.Warning, "Lỗi nhập liệu", "Vui lòng nhập Key (Số hàng)!")
            return

        try:
            # Ép kiểu sang int để kiểm tra xem có phải số nguyên không
            key = int(key_input)
        except ValueError:
            self.show_message(QMessageBox.Warning, "Ràng buộc sai", "Key của thuật toán Rail Fence bắt buộc phải là một số nguyên!")
            return

        # Kiểm tra điều kiện số hàng phải >= 2
        if key < 2:
            self.show_message(QMessageBox.Warning, "Ràng buộc sai", "Số hàng (Key) phải là số nguyên lớn hơn hoặc bằng 2!")
            return
        # ==================================================================

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key # Gửi đi dưới dạng số nguyên int đã chuẩn hóa
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
        # Lấy dữ liệu và xóa khoảng trắng thừa
        cipher_text = self.ui.txt_CipherText.toPlainText().strip()
        key_input = self.ui.txt_Key.text().strip()

        # ================= RÀNG BUỘC ĐẦU VÀO (VALIDATION) =================
        if not cipher_text:
            self.show_message(QMessageBox.Warning, "Lỗi nhập liệu", "Vui lòng nhập văn bản cần giải mã (Cipher Text)!")
            return

        if not key_input:
            self.show_message(QMessageBox.Warning, "Lỗi nhập liệu", "Vui lòng nhập Key (Số hàng)!")
            return

        try:
            key = int(key_input)
        except ValueError:
            self.show_message(QMessageBox.Warning, "Ràng buộc sai", "Key của thuật toán Rail Fence bắt buộc phải là một số nguyên!")
            return

        if key < 2:
            self.show_message(QMessageBox.Warning, "Ràng buộc sai", "Số hàng (Key) phải là số nguyên lớn hơn hoặc bằng 2!")
            return
        # ==================================================================

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key # Gửi đi dưới dạng số nguyên int đã chuẩn hóa
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