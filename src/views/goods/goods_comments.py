# comment_manager.py
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QWidget,
                             QHeaderView, QTableWidgetItem, QDialog, QDialogButtonBox, QMessageBox,QFormLayout)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen

# 导入评价数据生成模块
from datas.comments import comments
# 导入会员信息
from datas.members import members

DEFAULT_IMAGE_PATH = "resources/images/comments/default.jpg"

# 评价等级映射
RATING_MAP = {
    1: "⭐ \n非常差",
    2: "⭐⭐ \n一般",
    3: "⭐⭐⭐ \n满意",
    4: "⭐⭐⭐⭐ \n很好",
    5: "⭐⭐⭐⭐⭐ \n非常好"
}

# 构建用户昵称映射
user_nicknames = {member[0]: member[6] for member in members}  # 索引6是昵称


# 图片显示类（带放大镜功能）
class MagnifierLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.magnifier_size = 200
        self.magnifier_visible = False
        self.magnifier_pos = QPoint(0, 0)

    def enterEvent(self, event):
        self.magnifier_visible = True  # 通过这个变量来控制大图的显示
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.magnifier_visible = False
        self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        self.magnifier_pos = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.magnifier_visible or self.pixmap() is None:
            return

        pixmap = self.pixmap()
        if pixmap.isNull():
            return

        # 绘制放大镜
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算放大区域
        scale = 2.0
        source_size = self.magnifier_size / scale
        source_rect = QtCore.QRectF(
            self.magnifier_pos.x() - source_size / 2,
            self.magnifier_pos.y() - source_size / 2,
            source_size, source_size
        )

        # 限制在图像范围内
        if source_rect.left() < 0:
            source_rect.moveLeft(0)
        if source_rect.top() < 0:
            source_rect.moveTop(0)
        if source_rect.right() > pixmap.width():
            source_rect.moveRight(pixmap.width())
        if source_rect.bottom() > pixmap.height():
            source_rect.moveBottom(pixmap.height())

        # 放大镜位置（在鼠标右下方）
        magnifier_rect = QtCore.QRectF(
            self.magnifier_pos.x() + 20,
            self.magnifier_pos.y() + 20,
            self.magnifier_size, self.magnifier_size
        )

        # 绘制放大后的图像
        painter.drawPixmap(magnifier_rect, pixmap, source_rect)

        # 绘制放大镜边框
        painter.setPen(QPen(Qt.red, 2))
        painter.drawRect(magnifier_rect)

        # 绘制源位置指示框
        painter.setPen(QPen(Qt.red, 2))
        painter.drawRect(source_rect)

        # 绘制连接线
        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        painter.drawLine(
            source_rect.center(),
            magnifier_rect.topLeft() + QPoint(10, 10)
        )


class PaginationBar(QWidget):
    """
    分页控件
    保持按钮总数,标签名动态变化的按钮
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 1
        self.total_pages = 1
        self.max_buttons = 10  # 最多显示的页码按钮数量

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        # 上一页按钮
        self.prev_btn = QPushButton("上一页")
        self.prev_btn.setFixedSize(80, 30)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:disabled {
                background: #bdc3c7;
            }
        """)
        self.prev_btn.clicked.connect(self.go_prev)  # 点击上一页,连接对应槽函数
        layout.addWidget(self.prev_btn)

        # 页码按钮容器
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(5)
        layout.addLayout(self.buttons_layout)

        # 下一页按钮
        self.next_btn = QPushButton("下一页")
        self.next_btn.setFixedSize(80, 30)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:disabled {
                background: #bdc3c7;
            }
        """)
        self.next_btn.clicked.connect(self.go_next)  # 点击下一页,连接对应槽函数
        layout.addWidget(self.next_btn)

        # 总页数标签
        self.total_label = QLabel("")
        self.total_label.setFixedWidth(100)
        layout.addWidget(self.total_label)

        # 页面跳转
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(50)
        self.page_input.setPlaceholderText("页码")
        layout.addWidget(QLabel("跳转到:"))
        layout.addWidget(self.page_input)

        self.go_btn = QPushButton("跳转")
        self.go_btn.setFixedSize(60, 30)
        self.go_btn.setStyleSheet("""
            QPushButton {
                background: #2ecc71;
                color: white;
                border-radius: 4px;
                border: none;
            }
        """)
        self.go_btn.clicked.connect(self.go_to_page)
        layout.addWidget(self.go_btn)

        layout.addStretch()

    def setup(self, total_pages):
        """设置分页控件"""
        self.total_pages = max(1, total_pages)
        self.current_page = 1
        self.update_buttons()

    def update_buttons(self):
        """更新页码按钮"""
        # 清空现有按钮
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 计算起始和结束页码
        start_page = max(1, self.current_page - self.max_buttons // 2)
        end_page = min(self.total_pages, start_page + self.max_buttons - 1)

        # 如果页码不足，调整起始页码
        if end_page - start_page < self.max_buttons - 1:
            start_page = max(1, end_page - self.max_buttons + 1)

        # 添加页码按钮
        for page in range(start_page, end_page + 1):
            btn = QPushButton(str(page))
            btn.setFixedSize(30, 30)
            btn.setProperty("page", page)

            if page == self.current_page:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #e74c3c;
                        color: white;
                        border-radius: 4px;
                        border: none;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #3498db;
                        color: white;
                        border-radius: 4px;
                        border: none;
                    }
                    QPushButton:hover {
                        background: #2980b9;
                    }
                """)

            btn.clicked.connect(lambda _, p=page: self.go_to_page(p))
            self.buttons_layout.addWidget(btn)

        # 添加省略号（如果需要）
        if end_page < self.total_pages:
            dots = QLabel("...")
            self.buttons_layout.addWidget(dots)

        # 更新总页数标签
        self.total_label.setText(f"共 {self.total_pages} 页")

        # 更新按钮状态
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)

    def go_prev(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_buttons()
            self.parent().load_page(self.current_page)

    def go_next(self):
        """当前页面进到下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_buttons()
            self.parent().load_page(self.current_page)

    def go_to_page(self, page=None):
        """跳转到指定页码"""
        if page is None:
            try:
                page = int(self.page_input.text())
            except ValueError:
                return

        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.update_buttons()
            # 调用父组件的加载页面方法
            self.parent().load_page(page)
        self.page_input.clear()


# 评价详情对话框
class CommentDetailDialog(QDialog):
    """评价详情对话框"""

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("评价详情")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel("评价详细信息")
        title_label.setStyleSheet("font: bold 16pt 'Microsoft YaHei UI'; color:#2c3e50;")
        layout.addWidget(title_label)

        # 表单区域
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # 评价ID
        form_layout.addRow("评价ID:", QLabel(str(data[0])))

        # 评价等级
        rating = RATING_MAP.get(data[1], "未知")
        rating_label = QLabel(rating)
        rating_label.setStyleSheet("font-size: 14pt; color: #e67e22; font-weight: bold;")
        form_layout.addRow("评价等级:", rating_label)

        # 评价内容
        comment_label = QLabel(data[2])
        comment_label.setWordWrap(True)
        comment_label.setStyleSheet("background-color: #f9f9f9; padding: 10px; border-radius: 4px;")
        form_layout.addRow("评价内容:", comment_label)

        # 订单号
        form_layout.addRow("订单号:", QLabel(str(data[4])))

        # 用户ID和昵称
        user_id = data[5]
        nickname = user_nicknames.get(user_id, f"用户{user_id}")
        user_label = QLabel(f"{user_id} ({nickname})")
        form_layout.addRow("用户ID:", user_label)

        # 创建时间和更新时间
        form_layout.addRow("创建时间:", QLabel(data[6]))
        form_layout.addRow("更新时间:", QLabel(data[7]))

        # 图片
        image_layout = QVBoxLayout()
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(200)

        image_path = data[3]
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)

        pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        image_layout.addWidget(image_label)
        form_layout.addRow("评价图片:", image_layout)

        layout.addLayout(form_layout)

        # 关闭按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        self.setLayout(layout)


class CommentListWidget(QWidget):
    """商品评价管理组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.search_keyword = ""
        self.current_page = 1
        self.per_page = 15
        self.total_pages = 1

        # 初始化分页控件
        self.pagination_bar = PaginationBar(self)
        self.bottom_layout.addWidget(self.pagination_bar)

        # 加载数据
        self.load_data()

    def setupUi(self):
        """初始化界面布局"""
        self.resize(1200, 800)

        # 主垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # 顶部操作栏
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel("商品评价管理")
        title_label.setStyleSheet("font: bold 16pt 'Microsoft YaHei UI'; color:#2c3e50;")
        top_layout.addWidget(title_label)

        top_layout.addStretch()

        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入订单号、用户ID或评价内容...")
        self.search_input.setFixedWidth(300)
        self.search_input.setStyleSheet("padding: 5px; border: 1px solid #ddd; border-radius: 4px;")
        top_layout.addWidget(self.search_input)

        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setFixedSize(80, 35)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        self.search_btn.clicked.connect(self.on_search)
        top_layout.addWidget(self.search_btn)

        # 批量删除按钮
        self.batch_del_btn = QPushButton("批量删除")
        self.batch_del_btn.setFixedSize(100, 35)
        self.batch_del_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        self.batch_del_btn.clicked.connect(self.on_batch_delete)
        top_layout.addWidget(self.batch_del_btn)

        main_layout.addWidget(top_widget)

        # 表格区域
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setStyleSheet("""
            QTableWidget {
                gridline-color: #eee;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.table_widget)

        # 底部布局（分页控件）
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 10, 0, 10)
        main_layout.addLayout(self.bottom_layout)

        # 初始化表格
        self.initTable()

    def initTable(self):
        """初始化表格"""
        headers = [
            "选择", "评价ID", "评价等级", "评价内容",
            "评价图片", "订单号", "用户",
            "创建时间", "修改时间", "操作"
        ]

        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSortingEnabled(True)

        # 设置列宽策略
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(0, 50)  # 选择列

        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(1, 80)  # 评价ID

        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(2, 150)  # 评价等级

        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)  # 评价内容

        self.table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(4, 220)  # 评价图片

        self.table_widget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(5, 220)  # 订单号

        self.table_widget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(6, 150)  # 用户

        self.table_widget.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(7, 200)  # 创建时间

        self.table_widget.horizontalHeader().setSectionResizeMode(8, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(8, 200)  # 修改时间

        self.table_widget.horizontalHeader().setSectionResizeMode(9, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(9, 180)  # 操作

    def load_data(self):
        """加载数据并更新分页"""
        # 倒序排列
        sorted_comments = sorted(comments, key=lambda x: x[0], reverse=True)

        # 计算分页
        self.total_items = len(sorted_comments)
        self.total_pages = max(1, (self.total_items + self.per_page - 1) // self.per_page)

        # 设置分页控件
        self.pagination_bar.setup(self.total_pages)

        # 加载当前页数据
        self.load_page(1)

    def load_page(self, page):
        """加载指定页的数据"""
        self.current_page = page

        # 倒序排列
        sorted_comments = sorted(comments, key=lambda x: x[0], reverse=True)

        # 过滤数据
        if self.search_keyword:
            filtered_data = []
            for c in sorted_comments:
                nickname = user_nicknames.get(c[5], f"用户{c[5]}")
                if (str(c[4]).find(self.search_keyword) != -1 or
                        str(c[5]).find(self.search_keyword) != -1 or
                        nickname.find(self.search_keyword) != -1 or
                        c[2].find(self.search_keyword) != -1):
                    filtered_data.append(c)
        else:
            filtered_data = sorted_comments

        # 计算分页范围
        start_idx = (page - 1) * self.per_page
        end_idx = min(start_idx + self.per_page, len(filtered_data))
        page_data = filtered_data[start_idx:end_idx]

        # 清空表格
        self.table_widget.setRowCount(0)

        # 添加行数据
        for idx, data in enumerate(page_data):
            self.add_table_row(idx, data)

    def add_table_row(self, row_idx, data):
        """添加表格行"""
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setRowHeight(row, 80)

        # 复选框
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left:10px;")
        self.table_widget.setCellWidget(row, 0, checkbox)

        # 评价ID
        item = QTableWidgetItem(str(data[0]))
        item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 1, item)

        # 评价等级（星级显示）
        rating = RATING_MAP.get(data[1], "未知")
        rating_item = QTableWidgetItem(rating)
        rating_item.setTextAlignment(Qt.AlignCenter)

        # 根据评分设置颜色
        if data[1] >= 4:
            rating_item.setForeground(QColor("#27ae60"))  # 绿色
        elif data[1] == 3:
            rating_item.setForeground(QColor("#f39c12"))  # 橙色
        else:
            rating_item.setForeground(QColor("#e74c3c"))  # 红色

        self.table_widget.setItem(row, 2, rating_item)

        # 评价内容
        comment = data[2]
        if len(comment) > 40:
            comment = comment[:40] + "..."

        comment_item = QTableWidgetItem(comment)
        comment_item.setToolTip(data[2])
        self.table_widget.setItem(row, 3, comment_item)

        # 评价图片
        if data[3]:
            self.set_image_cell(row, 4, data[3])

        # 订单号
        order_item = QTableWidgetItem(str(data[4]))
        order_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 5, order_item)

        # 用户信息（显示昵称）
        user_id = data[5]
        nickname = user_nicknames.get(user_id, f"用户{user_id}")
        user_item = QTableWidgetItem(nickname)
        user_item.setTextAlignment(Qt.AlignCenter)
        user_item.setToolTip(f"用户ID: {user_id}")
        self.table_widget.setItem(row, 6, user_item)

        # 创建时间
        create_time_item = QTableWidgetItem(data[6])
        create_time_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 7, create_time_item)

        # 修改时间
        update_time_item = QTableWidgetItem(data[7])
        update_time_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 8, update_time_item)

        # 操作按钮
        widget = QWidget()
        btn_layout = QHBoxLayout(widget)
        btn_layout.setContentsMargins(5, 0, 5, 0)
        btn_layout.setSpacing(5)

        # 查看按钮
        view_btn = QPushButton("查看")
        view_btn.setFixedSize(60, 30)
        view_btn.setStyleSheet("""
            QPushButton {
                background: #9b59b6;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background: #8e44ad;
            }
        """)
        view_btn.clicked.connect(lambda _, id=data[0]: self.show_detail_dialog(id))
        btn_layout.addWidget(view_btn)

        # 删除按钮
        del_btn = QPushButton("删除")
        del_btn.setFixedSize(60, 30)
        del_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        del_btn.clicked.connect(lambda _, id=data[0]: self.delete_row(id))
        btn_layout.addWidget(del_btn)

        self.table_widget.setCellWidget(row, 9, widget)

    def set_image_cell(self, row, col, image_path):
        """设置图片单元格"""
        label = MagnifierLabel()
        
        # 检查图片路径是否存在，不存在则使用默认图片
        if os.path.exists(image_path):
            full_image_path = image_path
        else:
            full_image_path = DEFAULT_IMAGE_PATH
        
        # 把正确的图片路径存储为标签属性
        label.setProperty("full_image_path", full_image_path)
        
        pixmap = QPixmap(full_image_path)
        pixmap = pixmap.scaled(120, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        self.table_widget.setCellWidget(row, col, label)

    def on_search(self):
        """搜索评价"""
        keyword = self.search_input.text().strip()
        self.search_keyword = keyword
        self.load_data()

    def show_detail_dialog(self, item_id):
        """显示评价详情对话框"""
        target_data = next((c for c in comments if c[0] == item_id), None)
        if not target_data:
            QMessageBox.warning(self, "错误", "未找到评价信息")
            return

        dialog = CommentDetailDialog(self, target_data)
        dialog.exec()

    def delete_row(self, item_id):
        """删除单个评价"""
        reply = QMessageBox.question(self, "删除确认", "确定要删除该评价吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 从全局数据中删除
            global comments
            comments = [c for c in comments if c[0] != item_id]

            # 刷新列表
            self.load_data()

    def on_batch_delete(self):
        """批量删除评价"""
        selected_ids = []
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.cellWidget(row, 0).isChecked():
                item = self.table_widget.item(row, 1)
                if item:
                    selected_ids.append(int(item.text()))

        if not selected_ids:
            QMessageBox.warning(self, "提示", "请选择要删除的评价")
            return

        reply = QMessageBox.question(self, "批量删除",
                                     f"确定要删除选中的 {len(selected_ids)} 条评价吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 从全局数据中删除
            global comments
            comments = [c for c in comments if c[0] not in selected_ids]

            # 刷新列表
            self.load_data()


# 主程序入口
if __name__ == "__main__":
    APP = QApplication(sys.argv)

    # 创建主窗口
    main_window = QWidget()
    main_window.setWindowTitle("商品评价管理系统")
    main_window.resize(1200, 800)

    # 添加评价管理组件
    layout = QVBoxLayout(main_window)
    comment_widget = CommentListWidget()
    layout.addWidget(comment_widget)

    main_window.show()
    sys.exit(APP.exec())
