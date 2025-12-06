# coding=utf-8
import os.path
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import sys

current_dir = os.path.dirname(__file__)
ui_path = os.path.join(current_dir, "reg.ui")

if not os.path.exists(ui_path):
    print(f"错误2222：文件 {ui_path} 不存在！")
else:
    Ui_RegWindow = uic.loadUiType(ui_path)[0]


class RegDialog(QtWidgets.QDialog, Ui_RegWindow):
    def __init__(self, a0: int):
        super(RegDialog, self).__init__(a0)
        self.setupUi(self)
        self.initUi()
        self.initQSS()

    def initQSS(self):
        '''
        初始化样式
        '''
        style_file = QFile(os.path.join("source/style/style_back.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            style_sheet = stream.readAll()
            # print(style_sheet)
            self.setStyleSheet(style_sheet)

    def initUi(self):
        '''
        初始化表单
        '''
        self.reg_ok_pushButton.setProperty('class', 'QPushButton_Primary')
        self.reg_cancel_pushButton.setProperty('class', 'QPushButton_Cancel')
        self.reg_ok_pushButton.clicked.connect(self.slot_ok)  # 点击确定按钮
        self.reg_cancel_pushButton.clicked.connect(self.slot_cancel)  # 点击确定按钮

    def save_reg_info(self, user, pwd):
        return True

    def slot_cancel(self):
        '''
        取消按钮事件响应
        '''
        self.close()

    def slot_ok(self):
        user = self.reg_user_lineEdit.text()
        pwd = self.reg_pwd_lineEdit.text()
        if user == '' or pwd == '':
            pass
        else:
            self.save_reg_info(user, pwd)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reg_dialog = RegDialog()
    reg_dialog.show()
    sys.exit(app.exec_())
