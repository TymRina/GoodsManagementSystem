import random
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QWidget,
                             QHeaderView, QTableWidgetItem, QDialog, QDialogButtonBox, QFileDialog, QMessageBox,
                             QComboBox, QRadioButton, QButtonGroup, QGridLayout, QFormLayout)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen, QBrush
from datetime import datetime
import uuid
import re

# 导入数据库管理模块
from src.modules.database import db_manager
from src.modules.goods_manager import goods_manager
from src.modules.category_manager import category_manager, brand_manager

DEFAULT_IMAGE_PATH = "resources/images/goods/default.jpg"

# 状态映射
STATUS_MAP = {
    0: "下架",
    1: "上架"
}


# # 图片显示类
# class MagnifierLabel(QLabel):  # 注意父类为QLabel
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setMouseTracking(True)
#         self.magnifier_size = 200
#         self.magnifier_visible = False
#         self.magnifier_pos = QPoint(0, 0)
#
#     def enterEvent(self, event):
#         self.magnifier_visible = True
#         self.update()
#         super().enterEvent(event)
#
#     def leaveEvent(self, event):
#         self.magnifier_visible = False
#         self.update()
#         super().leaveEvent(event)
#
#     def mouseMoveEvent(self, event):
#         self.magnifier_pos = event.pos()  # 跟随鼠标移动
#         self.update()
#         super().mouseMoveEvent(event)
#
#     def paintEvent(self, event):
#         super().paintEvent(event)
#
#         if not self.magnifier_visible or self.pixmap() is None:
#             return
#
#         pixmap = self.pixmap()
#         if pixmap.isNull():
#             return
#
#         # 绘制放大镜
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         # 参数self指定绘图目标表面，通常是QWidget或其子类,这里是QLabel的子类
#         # QWidget表面限制‌：当QPainter绑定到QWidget或其子类(如QLabel)时，绘图操作受限于该控件的几何边界。
#         # 这是Qt绘图系统的基本机制，所有绘制内容都会被自动裁剪到目标表面的可见区域。
#         # 因此创建独立于QLabel的独立窗口来显示是最简单的,但是需要图片文件以及它的路径,
#         # 我们有
#         # image_path = data[9]
#         # if os.path.exists(image_path):
#         #   pixmap = QPixmap(image_path)
#         # else:
#         #   pixmap = QPixmap(DEFAULT_IMAGE_PATH)
#         # 采用之前简单项目的独立窗口大图的方式,重写这个类
#
#
#
#         # 计算放大区域
#         scale = 2.0  # 缩放比
#         source_size = self.magnifier_size / scale  # 源区域大小
#         source_rect = QtCore.QRectF(
#             self.magnifier_pos.x() - source_size / 2,
#             self.magnifier_pos.y() - source_size / 2,
#             source_size, source_size
#         )
#
#         # 限制源区域在图像范围内,超出边界则移动回来
#         # (边界限制的必要性!!!)
#         # 注释掉这些操作会导致绘制的图片和放大区域不匹配,为什么?
#         # 当source_rect超出图像边界时，Qt会尝试从无效内存区域读取像素数据
#         # 如果源区域越界，实际参与绘制的有效区域会缩小
#         # 但目标区域(magnifier_rect)仍保持原尺寸，导致内容拉伸失真
#         if source_rect.left() < 0:
#             source_rect.moveLeft(0)
#         if source_rect.top() < 0:
#             source_rect.moveTop(0)
#         if source_rect.right() > pixmap.width():
#             source_rect.moveRight(pixmap.width())
#         if source_rect.bottom() > pixmap.height():
#             source_rect.moveBottom(pixmap.height())
#
#         # 放大镜位置（在鼠标右下方）(显示区域)
#         magnifier_rect = QtCore.QRectF(
#             self.magnifier_pos.x() + 20,
#             self.magnifier_pos.y() + 20,
#             self.magnifier_size, self.magnifier_size
#         )
#
#         # 绘制放大后的图像
#         painter.drawPixmap(magnifier_rect, pixmap, source_rect)
#
#         # 绘制放大镜边框
#         painter.setPen(QPen(Qt.red, 2))
#         painter.drawRect(magnifier_rect)
#
#         # 绘制源位置指示框(在原始图像上)
#         painter.setPen(QPen(Qt.red, 2))
#         painter.drawRect(source_rect)
#
#         # 绘制连接线
#         painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
#         painter.drawLine(
#             source_rect.center(),
#             magnifier_rect.topLeft() + QPoint(10, 10)
#         )

# 图片显示类
class MagnifierLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fullsize_label = QLabel()
        self.fullsize_label.setWindowFlag(Qt.ToolTip)

        # 内容缩放
        self.fullsize_label.setScaledContents(True)
        # 事件过滤器
        self.installEventFilter(self)
        # 获取屏幕尺寸
        self.screen_rect = QApplication.desktop().availableGeometry()

    # 事件过滤器(重写)
    def eventFilter(self, obj, event):
        # Enter鼠标进入事件
        if event.type() == QtCore.QEvent.Enter:
            print('enter')
            full_image_path = self.property("full_image_path")
            print(full_image_path)
            pixmap = QPixmap(full_image_path) if full_image_path else QPixmap(DEFAULT_IMAGE_PATH)

            if not pixmap.isNull():
                self.fullsize_label.setPixmap(pixmap.scaled(400, 400))
                # 获取当前鼠标的位置，默认把图片显示在鼠标位置的右下方(偏移)
                cursor_pos = QtGui.QCursor.pos()
                pos = cursor_pos + QPoint(20, 20)
                label_size = self.fullsize_label.size()
                # 想让图片永远在屏幕内,不出屏幕(不出窗口的话类似可做)
                # 检查右侧边界
                if pos.x() + label_size.width() > self.screen_rect.right():
                    pos.setX(cursor_pos.x() - label_size.width() - 20)

                # 检查底部边界
                if pos.y() + label_size.height() > self.screen_rect.bottom():
                    pos.setY(cursor_pos.y() - label_size.height() - 20)

                print('pos', pos)
                self.fullsize_label.move(pos)
                self.fullsize_label.show()

        # 鼠标离开
        elif event.type() == QtCore.QEvent.Leave:
            print('leave')
            self.fullsize_label.hide()

        return super().eventFilter(obj, event)




class PaginationBar(QWidget):
    """分页控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 1   # 当前页码，默认为1
        self.total_pages = 1  # 总页数，默认为1
        self.max_buttons = 10  # 最多显示的页码按钮数量

        layout = QHBoxLayout(self)  # 使用水平布局
        layout.setContentsMargins(0, 5, 0, 5)  # 设置布局边距

        # 创建"上一页"按钮
        self.prev_btn = QPushButton("上一页")
        self.prev_btn.setFixedSize(80, 30)  # 固定按钮大小
        # 设置按钮样式
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background: #3498db; /* 默认蓝色背景 */
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:disabled {
                background: #bdc3c7; /* 禁用时灰色背景 */
            }
        """)
        self.prev_btn.clicked.connect(self.go_prev)  # 绑定点击事件,槽函数为'去上一页'
        layout.addWidget(self.prev_btn)  # 添加到布局

        # 创建页码按钮容器布局(就是放1,2,3...这些页码按钮的)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(5)  # 设置按钮间距
        layout.addLayout(self.buttons_layout)

        # 下一页按钮
        self.next_btn = QPushButton("下一页")
        self.next_btn.setFixedSize(80, 30)
        # 设置与上一页相同的样式
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
        self.next_btn.clicked.connect(self.go_next)
        layout.addWidget(self.next_btn)

        # 创建总页数标签
        self.total_label = QLabel("")
        self.total_label.setFixedWidth(100)
        layout.addWidget(self.total_label)

        # 创建页面跳转输入框
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(50)
        self.page_input.setPlaceholderText("页码")  # 设置占位文本
        layout.addWidget(QLabel("跳转到:"))  # 添加标签
        layout.addWidget(self.page_input)

        # 创建跳转按钮
        self.go_btn = QPushButton("跳转")
        self.go_btn.setFixedSize(60, 30)
        # 设置绿色样式
        self.go_btn.setStyleSheet("""
            QPushButton {
                background: #2ecc71;
                color: white;
                border-radius: 4px;
                border: none;
            }
        """)
        # 使用lambda表达式忽略clicked信号传递的布尔值参数
        self.go_btn.clicked.connect(lambda: self.go_to_page())
        layout.addWidget(self.go_btn)

        layout.addStretch()  # 添加伸缩项，使控件靠左对齐

    def setup(self, total_pages):
        """设置分页控件"""
        self.total_pages = max(1, total_pages)  # 确保至少有1页
        self.current_page = 1  # 重置当前页为第1页
        self.update_buttons()  # 更新按钮状态

    def update_buttons(self):
        """更新页码按钮"""
        # 清空现有按钮
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 计算要显示的起始和结束页码
        # 当前页居中显示，前后各显示max_buttons//2个按钮
        start_page = max(1, self.current_page - self.max_buttons // 2)
        end_page = min(self.total_pages, start_page + self.max_buttons - 1)

        # 如果页码不足max_buttons个，调整起始页码
        if end_page - start_page < self.max_buttons - 1:
            start_page = max(1, end_page - self.max_buttons + 1)

        # 添加页码按钮
        for page in range(start_page, end_page + 1):
            btn = QPushButton(str(page))
            btn.setFixedSize(30, 30)
            btn.setProperty("page", page)  # 设置自定义属性存储页码

            # 当前页按钮特殊样式(红色)
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
                # 非当前页按钮样式(蓝色，悬停效果)
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

            # 绑定点击事件，跳转到对应页码
            btn.clicked.connect(lambda _, p=page: self.go_to_page(p))
            self.buttons_layout.addWidget(btn)

        # 如果结束页码小于总页数，添加省略号
        if end_page < self.total_pages:
            dots = QLabel("...")
            self.buttons_layout.addWidget(dots)

        # 更新总页数标签
        self.total_label.setText(f"共 {self.total_pages} 页")

        # 更新上一页/下一页按钮状态
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)

    def go_prev(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_buttons()  # 更新按钮显示
            self.parent().load_page(self.current_page)  # 通知父组件加载数据

    def go_next(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_buttons()
            self.parent().load_page(self.current_page)

    def go_to_page(self, page=None):
        """跳转到指定页码"""
        if page is None:  # 如果没有传入页码，从输入框获取
            try:
                page = int(self.page_input.text())
            except ValueError:  # 输入无效时忽略
                return
        # 确保页码在有效范围内
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.update_buttons()
            self.parent().load_page(page)  # 通知父组件加载数据
        self.page_input.clear()  # 清空输入框


# 商品详情对话框
class ProductDetailDialog(QDialog):
    """商品详情对话框"""

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("商品详情")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel("商品详细信息")
        title_label.setStyleSheet("font: bold 16pt 'Microsoft YaHei UI'; color:#2c3e50;")
        layout.addWidget(title_label)

        # 表单区域
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # 商品ID
        form_layout.addRow("商品ID:", QLabel(str(data.get('id', ''))))

        # 商品标题
        form_layout.addRow("商品标题:", QLabel(data.get('title', '')))

        # 商品编码
        form_layout.addRow("商品编码:", QLabel(data.get('code', '')))

        # 分类
        cat_name = category_manager.get_category_path(data.get('category_id', 0))
        form_layout.addRow("商品分类:", QLabel(cat_name))

        # 品牌名称
        brands = brand_manager.get_all_brands()
        brand_name = next((b['name'] for b in brands if b['id'] == data.get('brand_id', 0)), "未知品牌")
        form_layout.addRow("商品品牌:", QLabel(brand_name))

        # 价格
        form_layout.addRow("售价(元):", QLabel(f"{data.get('sale_price', 0):.2f}"))
        form_layout.addRow("原价(元):", QLabel(f"{data.get('original_price', 0):.2f}"))

        # 库存
        form_layout.addRow("库存数量:", QLabel(str(data.get('stock', 0))))

        # 状态
        status = STATUS_MAP.get(data.get('status', 0), "未知")
        status_label = QLabel(status)
        if data.get('status', 0) == 1:  # 上架
            status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        elif data.get('status', 0) == 0:  # 下架
            status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        form_layout.addRow("商品状态:", status_label)

        # 创建时间和更新时间
        form_layout.addRow("创建时间:", QLabel(str(data.get('create_time', ''))))
        form_layout.addRow("更新时间:", QLabel(str(data.get('update_time', ''))))

        # 图片
        image_layout = QVBoxLayout()
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)

        image_path = data.get('image_path', DEFAULT_IMAGE_PATH)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)

        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        image_layout.addWidget(image_label)
        form_layout.addRow("商品图片:", image_layout)

        layout.addLayout(form_layout)

        # 关闭按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        self.setLayout(layout)


class ProductDialog(QDialog):
    """商品添加/编辑对话框"""

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("添加商品" if not data else "编辑商品")
        self.setFixedSize(700, 600)
        self.image_path = data.get('image_path', DEFAULT_IMAGE_PATH) if data else DEFAULT_IMAGE_PATH
        self.goods_data = data

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题区域
        title_layout = QHBoxLayout()
        title_label = QLabel("商品信息")
        title_label.setStyleSheet("font: bold 16pt 'Microsoft YaHei UI'; color:#2c3e50;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 表单区域
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)

        # 商品标题
        row = 0
        form_layout.addWidget(QLabel("商品标题:"), row, 0, Qt.AlignRight)
        self.title_edit = QLineEdit(data.get('title', '') if data else "")
        self.title_edit.setPlaceholderText("请输入商品标题（不少于10个字）")
        form_layout.addWidget(self.title_edit, row, 1, 1, 2)

        # 分类选择
        row += 1
        form_layout.addWidget(QLabel("商品分类:"), row, 0, Qt.AlignRight)

        # 一级分类
        self.level1_combo = QComboBox()
        self.level1_combo.addItem("--请选择一级分类--", None)
        for category in category_manager.get_subcategories(0):
            self.level1_combo.addItem(category['name'], category['id'])
        self.level1_combo.currentIndexChanged.connect(self.update_level2)
        form_layout.addWidget(self.level1_combo, row, 1)

        # 二级分类
        self.level2_combo = QComboBox()
        self.level2_combo.addItem("--请选择二级分类--", None)
        self.level2_combo.currentIndexChanged.connect(self.update_level3)
        self.level2_combo.setEnabled(False)
        form_layout.addWidget(self.level2_combo, row, 2)

        # 三级分类
        row += 1
        self.level3_combo = QComboBox()
        self.level3_combo.addItem("--请选择三级分类--", None)
        self.level3_combo.setEnabled(False)
        form_layout.addWidget(QLabel(""), row, 0)  # 空标签占位
        form_layout.addWidget(self.level3_combo, row, 1, 1, 2)

        # 品牌选择
        row += 1
        form_layout.addWidget(QLabel("商品品牌:"), row, 0, Qt.AlignRight)
        self.brand_combo = QComboBox()
        self.brand_combo.addItem("--请选择品牌--", None)
        # 从数据库获取品牌
        brands = brand_manager.get_all_brands()
        for brand in brands:
            self.brand_combo.addItem(brand['name'], brand['id'])
        # 初始化品牌选择
        if data:
            brand_id = data.get('brand_id')
            if brand_id:
                for idx in range(self.brand_combo.count()):
                    if self.brand_combo.itemData(idx) == brand_id:
                        self.brand_combo.setCurrentIndex(idx)
                        break
        form_layout.addWidget(self.brand_combo, row, 1, 1, 2)

        # 价格区域
        row += 1
        price_layout = QHBoxLayout()
        price_layout.setSpacing(10)

        # 原价
        price_layout.addWidget(QLabel("原价:"))
        self.original_price_edit = QLineEdit(str(data.get('original_price', 0)) if data else "")
        self.original_price_edit.setPlaceholderText("0.00")
        self.original_price_edit.setValidator(QtGui.QDoubleValidator(0, 999999, 2))
        price_layout.addWidget(self.original_price_edit)

        # 售价
        price_layout.addWidget(QLabel("售价:"))
        self.sale_price_edit = QLineEdit(str(data.get('sale_price', 0)) if data else "")
        self.sale_price_edit.setPlaceholderText("0.00")
        self.sale_price_edit.setValidator(QtGui.QDoubleValidator(0, 999999, 2))
        price_layout.addWidget(self.sale_price_edit)

        form_layout.addLayout(price_layout, row, 1, 1, 2)
        form_layout.addWidget(QLabel("价格(元):"), row, 0, Qt.AlignRight)

        # 状态选择
        row += 1
        form_layout.addWidget(QLabel("商品状态:"), row, 0, Qt.AlignRight)
        status_layout = QHBoxLayout()
        self.status_group = QButtonGroup(self)

        self.status_on = QRadioButton("上架")
        self.status_on.setChecked(True)
        self.status_group.addButton(self.status_on, 1)
        status_layout.addWidget(self.status_on)

        self.status_off = QRadioButton("下架")
        self.status_group.addButton(self.status_off, 0)
        status_layout.addWidget(self.status_off)

        if data:
            if data.get('status', 1) == 0:
                self.status_off.setChecked(True)
            else:
                self.status_on.setChecked(True)

        form_layout.addLayout(status_layout, row, 1, 1, 2)

        # 图片上传
        row += 1
        form_layout.addWidget(QLabel("商品图片:"), row, 0, Qt.AlignTop | Qt.AlignRight)

        image_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(180, 180)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px dashed #ccc;")
        self.update_image()
        image_layout.addWidget(self.image_label)

        btn_upload = QPushButton("上传图片")
        btn_upload.setFixedSize(100, 30)
        btn_upload.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 4px;
                border: none;
            }
        """)
        btn_upload.clicked.connect(self.upload_image)
        image_layout.addWidget(btn_upload, 0, Qt.AlignCenter)

        form_layout.addLayout(image_layout, row, 1, 1, 2)

        layout.addLayout(form_layout)

        # 错误提示
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # 按钮组
        btn_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        btn_box.rejected.connect(self.reject)
        btn_box.accepted.connect(self.validate_and_accept)
        layout.addWidget(btn_box)

        self.setLayout(layout)

        # 如果是编辑模式，设置分类和品牌
        if data:
            # 设置分类
            self.set_category(data.get('category_id'))
            # 设置品牌
            brand_id = data.get('brand_id')
            if brand_id:
                for idx in range(self.brand_combo.count()):
                    if self.brand_combo.itemData(idx) == brand_id:
                        self.brand_combo.setCurrentIndex(idx)
                        break

    def set_category(self, cat_id):
        """设置分类选择"""
        # 获取分类信息
        category = category_manager.get_category_by_id(cat_id)
        if not category:
            return
            
        path = []
        current_id = cat_id
        
        # 构建分类路径
        while current_id != 0:
            category = category_manager.get_category_by_id(current_id)
            if not category:
                break
            path.insert(0, (category['id'], category['name']))
            current_id = category['parent_id']

        # 设置分类选择
        if len(path) >= 1:
            # 一级分类
            for idx in range(self.level1_combo.count()):
                if self.level1_combo.itemData(idx) == path[0][0]:
                    self.level1_combo.setCurrentIndex(idx)
                    self.update_level2()
                    break

            if len(path) >= 2:
                # 二级分类
                for idx in range(self.level2_combo.count()):
                    if self.level2_combo.itemData(idx) == path[1][0]:
                        self.level2_combo.setCurrentIndex(idx)
                        self.update_level3()
                        break

                if len(path) >= 3:
                    # 三级分类
                    for idx in range(self.level3_combo.count()):
                        if self.level3_combo.itemData(idx) == path[2][0]:
                            self.level3_combo.setCurrentIndex(idx)
                            break

    def update_level2(self):
        """更新二级分类选项"""
        self.level2_combo.clear()
        self.level2_combo.addItem("--请选择二级分类--", None)

        level1_id = self.level1_combo.currentData()
        if level1_id:
            self.level2_combo.setEnabled(True)
            # 从数据库获取二级分类
            level2_categories = category_manager.get_subcategories(level1_id)
            for category in level2_categories:
                self.level2_combo.addItem(category['name'], category['id'])
        else:
            self.level2_combo.setEnabled(False)

        # 重置三级分类
        self.level3_combo.clear()
        self.level3_combo.addItem("--请选择三级分类--", None)
        self.level3_combo.setEnabled(False)

    def update_level3(self):
        """更新三级分类选项"""
        self.level3_combo.clear()
        self.level3_combo.addItem("--请选择三级分类--", None)

        level1_id = self.level1_combo.currentData()
        level2_id = self.level2_combo.currentData()

        if level1_id and level2_id:
            self.level3_combo.setEnabled(True)
            # 从数据库获取三级分类
            level3_categories = category_manager.get_subcategories(level2_id)
            for category in level3_categories:
                self.level3_combo.addItem(category['name'], category['id'])
        else:
            self.level3_combo.setEnabled(False)

    def upload_image(self):
        """上传图片"""
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件(*.png *.jpg *.jpeg)")

        if path:
            try:
                # 创建保存目录到resources/images/goods
                save_dir = os.path.join("resources", "images", "goods")
                os.makedirs(save_dir, exist_ok=True)

                # 生成唯一文件名
                file_ext = os.path.splitext(path)[1]
                file_name = f"{uuid.uuid4().hex}{file_ext}"
                save_path = os.path.join(save_dir, file_name)

                # 保存图片
                pixmap = QPixmap(path)
                if pixmap.save(save_path):
                    self.image_path = save_path
                    self.update_image()
                else:
                    self.error_label.setText("图片保存失败")
            except Exception as e:
                self.error_label.setText(f"错误: {str(e)}")

    def update_image(self):
        """更新图片显示"""
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)

        pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def validate_and_accept(self):
        """验证表单并接受"""
        # 重置错误信息
        self.error_label.setText("")

        # 验证标题
        title = self.title_edit.text().strip()
        if len(title) < 10:
            self.error_label.setText("商品标题不能少于10个字")
            return

        # 验证分类
        level1_id = self.level1_combo.currentData()
        if not level1_id:
            self.error_label.setText("请至少选择一级分类")
            return

        level2_id = self.level2_combo.currentData()
        level3_id = self.level3_combo.currentData()

        # 获取最终分类ID
        cat_id = category_manager.get_category_id(level1_id, level2_id, level3_id)
        if not cat_id:
            self.error_label.setText("请选择有效的分类")
            return

        # 验证品牌
        brand_id = self.brand_combo.currentData()
        if not brand_id:
            self.error_label.setText("请选择品牌")
            return

        # 验证价格
        try:
            original_price = float(self.original_price_edit.text())
            sale_price = float(self.sale_price_edit.text())
            if original_price <= 0 or sale_price <= 0:
                self.error_label.setText("价格必须大于0")
                return
            if sale_price > original_price:
                self.error_label.setText("售价不能高于原价")
                return
        except ValueError:
            self.error_label.setText("请输入有效的价格")
            return

        # 所有验证通过
        self.accept()

    def get_goods_data(self):
        """获取商品数据"""
        # 获取分类ID
        level1_id = self.level1_combo.currentData()
        level2_id = self.level2_combo.currentData()
        level3_id = self.level3_combo.currentData()
        cat_id = category_manager.get_category_id(level1_id, level2_id, level3_id)

        # 库存随机生成（100-99999）
        stock = random.randint(100, 99999)

        return {
            "title": self.title_edit.text(),
            "category_id": cat_id,
            "brand_id": self.brand_combo.currentData(),
            "original_price": float(self.original_price_edit.text()),
            "sale_price": float(self.sale_price_edit.text()),
            "stock": stock,
            "status": self.status_group.checkedId(),
            "image_path": self.image_path,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if not self.goods_data else self.goods_data.get('create_time'),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


class GoodsListWidget(QWidget):
    """商品管理组件"""

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
        title_label = QLabel("商品列表")
        title_label.setStyleSheet("font: bold 16pt 'Microsoft YaHei UI'; color:#2c3e50;")
        top_layout.addWidget(title_label)

        top_layout.addStretch()

        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入商品标题关键字...")
        self.search_input.setFixedWidth(280)
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

        # 添加商品按钮
        self.add_btn = QPushButton("添加商品")
        self.add_btn.setFixedSize(100, 35)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: #2ecc71;
                color: white;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background: #27ae60;
            }
        """)
        self.add_btn.clicked.connect(self.show_add_dialog)
        top_layout.addWidget(self.add_btn)

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
            "选择", "商品ID", "商品标题", "商品图片",
            "分类", "品牌", "售价(元)", "原价(元)",
            "库存", "状态", "创建时间", "操作"
        ]

        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSortingEnabled(True)

        # 设置列宽策略
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(0, 50)

        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(1, 80)

        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(3, 150)

        self.table_widget.horizontalHeader().setSectionResizeMode(10, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(10, 150)

        self.table_widget.horizontalHeader().setSectionResizeMode(11, QHeaderView.Fixed)
        self.table_widget.setColumnWidth(11, 240)

    def load_data(self):
        """加载数据并更新分页"""
        # 从数据库获取所有商品
        all_goods = goods_manager.get_all_goods()

        # 过滤数据
        if self.search_keyword:
            filtered_data = [g for g in all_goods if self.search_keyword.lower() in g['title'].lower()]
        else:
            filtered_data = all_goods

        # 计算分页
        self.total_items = len(filtered_data)
        self.total_pages = max(1, (self.total_items + self.per_page - 1) // self.per_page)

        # 设置分页控件
        self.pagination_bar.setup(self.total_pages)

        # 加载当前页数据
        self.load_page(1)

    def load_page(self, page):
        """加载指定页的数据"""
        self.current_page = page

        # 从数据库获取所有商品
        all_goods = goods_manager.get_all_goods()

        # 过滤数据
        if self.search_keyword:
            filtered_data = [g for g in all_goods if self.search_keyword.lower() in g['title'].lower()]
        else:
            filtered_data = all_goods

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
        self.table_widget.setRowHeight(row, 100)

        # 复选框
        checkbox = QCheckBox()
        checkbox.setStyleSheet("margin-left:10px;")
        self.table_widget.setCellWidget(row, 0, checkbox)

        # 商品ID
        item = QTableWidgetItem(str(data['id']))
        item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 1, item)

        # 商品标题（高亮搜索关键词）
        title = data['title']
        if self.search_keyword:
            # 使用正则表达式进行不区分大小写的匹配
            pattern = re.compile(f"({re.escape(self.search_keyword)})", re.IGNORECASE)
            title = pattern.sub(r'<span style="background-color: #ffff00; font-weight: bold;">\1</span>', title)

        title_item = QTableWidgetItem()
        title_item.setData(Qt.DisplayRole, data['title'])
        title_item.setData(Qt.UserRole, data['title'])  # 保存原始标题
        title_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table_widget.setItem(row, 2, title_item)

        # 商品图片
        if data['image_path']:
            self.set_image_cell(row, 3, data['image_path'])

        # 分类名称
        cat_name = category_manager.get_category_path(data['category_id'])
        cat_item = QTableWidgetItem(cat_name)
        cat_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 4, cat_item)

        # 品牌名称
        brand = brand_manager.get_brand_by_id(data['brand_id'])
        brand_name = brand['name'] if brand else "未知品牌"
        brand_item = QTableWidgetItem(brand_name)
        brand_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 5, brand_item)

        # 售价
        sale_price_item = QTableWidgetItem(f"{data['sale_price']:.2f}")
        sale_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table_widget.setItem(row, 6, sale_price_item)

        # 原价
        original_price_item = QTableWidgetItem(f"{data['original_price']:.2f}")
        original_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table_widget.setItem(row, 7, original_price_item)

        # 库存
        stock_item = QTableWidgetItem(str(data['stock']))
        stock_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 8, stock_item)

        # 状态
        status = STATUS_MAP.get(data['status'], "未知")
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignCenter)
        if data['status'] == 1:  # 上架
            status_item.setForeground(QColor("#27ae60"))
        elif data['status'] == 0:  # 下架
            status_item.setForeground(QColor("#e74c3c"))
        self.table_widget.setItem(row, 9, status_item)

        # 创建时间
        create_time = data['create_time']
        if isinstance(create_time, datetime):
            create_time_str = create_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            create_time_str = str(create_time)
        create_time_item = QTableWidgetItem(create_time_str)
        create_time_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 10, create_time_item)

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
        view_btn.clicked.connect(lambda _, id=data['id']: self.show_detail_dialog(id))
        btn_layout.addWidget(view_btn)

        # 编辑按钮
        edit_btn = QPushButton("编辑")
        edit_btn.setFixedSize(60, 30)
        edit_btn.setStyleSheet("""
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
        edit_btn.clicked.connect(lambda _, id=data['id']: self.show_edit_dialog(id))
        btn_layout.addWidget(edit_btn)

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
        del_btn.clicked.connect(lambda _, id=data['id']: self.delete_row(id))
        btn_layout.addWidget(del_btn)

        self.table_widget.setCellWidget(row, 11, widget)

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
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        self.table_widget.setCellWidget(row, col, label)

    def on_search(self):
        """搜索商品"""
        keyword = self.search_input.text().strip()

        # 只有有搜索内容时才进行搜索
        if keyword:
            self.search_keyword = keyword
            self.load_data()
        else:
            # 清空搜索内容
            self.search_keyword = ""
            self.load_data()

    def show_add_dialog(self):
        """显示添加商品对话框"""
        dialog = ProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 获取新商品数据
            new_data = dialog.get_goods_data()

            # 添加到数据库
            goods_manager.add_goods(new_data)

            # 刷新列表
            self.load_data()

    def show_detail_dialog(self, item_id):
        # 从数据库查找商品数据
        target_data = goods_manager.get_goods_by_id(item_id)
        if not target_data:
            QMessageBox.warning(self, "错误", "未找到商品信息")
            return

        dialog = ProductDetailDialog(self, target_data)
        dialog.exec()

    def show_edit_dialog(self, item_id):
        # 从数据库查找商品数据
        target_data = goods_manager.get_goods_by_id(item_id)
        if not target_data:
            QMessageBox.warning(self, "错误", "未找到商品信息")
            return

        dialog = ProductDialog(self, target_data)
        if dialog.exec() == QDialog.Accepted:
            # 获取更新后的数据
            updated_data = dialog.get_goods_data()

            # 更新到数据库
            goods_manager.update_goods(item_id, updated_data)

            # 刷新列表
            self.load_data()

    def delete_row(self, item_id):
        """删除单个商品"""
        reply = QMessageBox.question(self, "删除确认", "确定要删除该商品吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 调用goods_manager删除商品
            goods_manager.delete_goods(item_id)
            # 刷新列表
            self.load_data()

    def on_batch_delete(self):
        """批量删除商品"""
        selected_ids = []
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.cellWidget(row, 0).isChecked():
                item = self.table_widget.item(row, 1)
                if item:
                    selected_ids.append(int(item.text()))

        if not selected_ids:
            QMessageBox.warning(self, "提示", "请选择要删除的商品")
            return

        reply = QMessageBox.question(self, "批量删除",
                                     f"确定要删除选中的 {len(selected_ids)} 个商品吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 从数据库中删除
            goods_manager.delete_goods_by_ids(selected_ids)

            # 刷新列表
            self.load_data()


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    window = GoodsListWidget()
    window.show()
    sys.exit(APP.exec())
