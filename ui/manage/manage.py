# coding =utf-8
from PyQt5 import  QtWidgets
import sys
import os
from PyQt5 import uic

current_dir = os.path.dirname(__file__)
ui_path = os.path.join(current_dir, "manage.ui")

page2_UI = uic.loadUiType(ui_path)[0]

class ManageWidget(QtWidgets.QWidget, page2_UI):
    '''
    中间内容区域的第一页模板
    '''
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        '''
        初始化表单
        '''
        # 提交及取消按钮样式及事件
        self.page2_ok_pushButton.setProperty('class', 'QPushButton_Primary')
        self.page2_cancel_pushButton.setProperty('class', 'QPushButton_Cancel')
        self.page2_ok_pushButton.clicked.connect(self.on_ok_clicked)
        self.page2_cancel_pushButton.clicked.connect(self.cancel_clicked)

    def on_ok_clicked(self):
        '''
        提交按钮点击事件响应方法
        '''
        print('点击了提交按钮!')

    def cancel_clicked(self):
        '''
        取消按钮点击事件响应方法
        '''
        print('点击了取消按钮!')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QFrame()
    win = ManageWidget(main)
    main.show()
    sys.exit(app.exec_())