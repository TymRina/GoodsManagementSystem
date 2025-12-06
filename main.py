import sys
import os

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置工作目录为当前文件所在目录
os.chdir(current_dir)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from src.views.login.login_view import LoginView
from src.views.home.home_view import HomeView


class AppController:
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__login_window = LoginView()
        self.__home_window = None

        # 连接信号
        self.__login_window.login_success.connect(self.__show_home)
        self.__login_window.show()

    def __show_home(self):
        self.__login_window.close()
        self.__home_window = HomeView()
        self.__home_window.show()

    def run(self):
        sys.exit(self.__app.exec_())


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    controller = AppController()
    controller.run()
