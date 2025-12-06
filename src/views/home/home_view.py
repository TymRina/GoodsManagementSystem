import os
import sys
import importlib
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QFile, QTextStream, QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
import qtawesome

from config.menu_config import MENU_CONFIGS
from datas.goods import goods
from datas.orders import orders
from datas.members import members

from src.views.goods.goods_list import GoodsListWidget
# from src.views.goods.goods_publish import GoodsPublishWidget


class HotReloadManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.last_mtime = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reload)
        self.timer.start(1000)
        self.reload_count = 0

    def check_reload(self):
        config_path = "config/menu_config.py"
        chart_config_path = "config/chart_config.py"
        style_path = "resources/styles/style.qss"

        for path in [config_path, chart_config_path, style_path]:
            try:
                if not os.path.exists(path):
                    continue

                mtime = os.path.getmtime(path)
                if self.last_mtime.get(path, 0) < mtime:
                    self.last_mtime[path] = mtime
                    self.handle_reload(path)
            except Exception as e:
                print(f"热重载错误: {str(e)}")

    def handle_reload(self, path):
        if path == "config/menu_config.py":
            importlib.reload(sys.modules['config.menu_config'])
            from config.menu_config import MENU_CONFIGS
            self.main_window.reload_menu(MENU_CONFIGS)
            print(f"[{self.reload_count}] 菜单配置已热更新")

        elif path == "resources/styles/style.qss":
            self.reload_style()
            print(f"[{self.reload_count}] 样式表已热更新")

        self.reload_count += 1
        self.force_gc()

    def reload_style(self):
        style_file = QFile("resources/styles/style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            style_sheet = stream.readAll()
            self.main_window.setStyleSheet(style_sheet)

    def force_gc(self):
        import gc
        gc.collect()
        if hasattr(QtCore, 'QCoreApplication'):
            QtCore.QCoreApplication.processEvents()


# 使用绝对路径加载UI文件
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
ui_file_path = os.path.join(project_root, "ui/layout/layout.ui")
Ui_MainWindow = uic.loadUiType(ui_file_path)[0]


class HomeView(QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.setWindowTitle("电商商品管理系统")
        self.setWindowIcon(QIcon('resources/icons/ico_main.png'))
        self.hot_reload = HotReloadManager(self)

        # 页面映射字典
        self.page_mapping = {}
        # 页面部件字典
        self.page_widgets = {}

        self.init_components()
        self.reload_menu(MENU_CONFIGS)
        self.reload_charts()
        self.init_styles()
        self.init_signals()

    def init_components(self):
        # 初始化页面映射
        self.init_page_mapping()

        # 初始化右侧页面
        self.init_page_widgets()

        # 初始化实时时钟
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_current_time)
        self.time_timer.start(1000)
        self.update_current_time()

    def init_page_mapping(self):
        # 首页
        self.page_mapping[0] = self.home_right_stackedWidget

        # 商品管理
        self.page_mapping[1] = self.goods_list_right_stackedWidget  # 商品列表
        self.page_mapping[2] = self.goods_publish_right_stackedWidget  # 商品发布
        self.page_mapping[3] = self.goods_comment_right_stackedWidget  # 商品评价
        self.page_mapping[4] = self.goods_category_right_stackedWidget  # 商品类别

        # 品牌管理
        self.page_mapping[5] = self.brand_list_right_stackedWidget  # 品牌列表

        # 订单管理
        self.page_mapping[6] = self.orders_list_right_stackedWidget  # 订单列表

        # 会员管理
        self.page_mapping[16] = self.members_list_right_stackedWidget  # 会员列表

        # 系统管理
        self.page_mapping[20] = self.role_list_right_stackedWidget  # 角色管理
        self.page_mapping[21] = self.permission_list_right_stackedWidget  # 权限管理
        self.page_mapping[23] = self.charts_list_right_stackedWidget  # 日志管理
        self.page_mapping[24] = self.charts_list_right_stackedWidget  # 数据备份

    def init_page_widgets(self):
        # 首页
        self.page_widgets[0] = HomeWidget(self)
        self.home_right_st_horizontalLayout.addWidget(self.page_widgets[0])

        # 商品列表
        self.page_widgets[1] = GoodsListWidget()
        self.goods_list_right_st_horizontalLayout.addWidget(self.page_widgets[1])

        # 商品发布
        # self.page_widgets[2] = GoodsPublishWidget()
        # self.goods_publish_right_st_horizontalLayout.addWidget(self.page_widgets[2])

        # 其他页面使用通用部件
        for page_id in self.page_mapping:
            if page_id not in self.page_widgets:
                self.page_widgets[page_id] = ChartsWidget()

                # 获取对应布局
                layout_name = self.page_mapping[page_id].objectName().replace("_stackedWidget", "_horizontalLayout")
                layout = getattr(self, layout_name, None)
                if layout:
                    layout.addWidget(self.page_widgets[page_id])

        # 设置当前页面为首页
        self.setStackCurrentPage(0)

    def init_styles(self):
        self.hot_reload.reload_style()

        for btn in self.findChildren(QtWidgets.QPushButton):
            if btn.objectName().startswith('left_button'):
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                    QPushButton:pressed {
                        background-color: #e0e0e0;
                    }
                """)

    def init_signals(self):
        self.top_toolButton1.clicked.connect(lambda: self.on_showpage_clicked(0))
        self.top_toolButton2.clicked.connect(lambda: self.on_showpage_clicked(20))  # 切换到系统管理页面
        self.top_toolButton3.clicked.connect(self.on_reg_clicked)
        self.top_toolButton4.clicked.connect(self.on_exit_clicked)

    def reload_menu(self, config):
        layout = self.left_widget_gridLayout
        # 清除现有菜单
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 重新创建菜单
        row = 0
        for group_idx, group in enumerate(config):
            # 添加分组标题
            subtitle = QtWidgets.QPushButton(group['title'])
            subtitle.setObjectName('left_subtitle_button')
            subtitle.setStyleSheet("""
                QPushButton {
                    color: #666;
                    font-weight: bold;
                    text-align: left;
                    padding: 12px 8px;
                    border: none;
                    background: transparent;
                }
            """)
            subtitle.setCursor(Qt.ArrowCursor)  # 禁止点击
            layout.addWidget(subtitle, row, 0)
            row += 1

            for item in group['items']:
                btn = QtWidgets.QPushButton(
                    qtawesome.icon(item['icon'], color='#666'),
                    item['name']
                )
                btn.setObjectName('left_menu_button')
                btn.setProperty('page', item['page'])
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        padding: 10px 15px;
                        margin: 2px 0;
                        border: none;
                        border-left: 3px solid transparent;
                        color: #444;
                    }
                    QPushButton:hover {
                        background-color: #f5f5f5;
                        border-left-color: #139667;
                    }
                    QPushButton:pressed {
                        background-color: #e0e0e0;
                    }
                """)
                # 确保连接正确的页面ID
                btn.clicked.connect(lambda _, p=item['page']: self.on_showpage_clicked(p))
                layout.addWidget(btn, row, 0)
                row += 1

    def reload_charts(self):
        """热重载时更新所有数据"""
        if 0 in self.page_widgets:
            home_widget = self.page_widgets[0]
            home_widget.update_all_data()
            print(f"[{self.hot_reload.reload_count}] 数据已热更新")

    def setStackCurrentPage(self, index):
        """设置当前显示的页面"""
        if index in self.page_mapping:
            widget = self.page_mapping[index]
            self.right_stackedWidget.setCurrentWidget(widget)
            print(f"切换到页面: {index}")

    def on_showpage_clicked(self, index):
        self.setStackCurrentPage(index)

    def on_reg_clicked(self):
        reg_dialog = RegDialog(self)
        reg_dialog.open()

    def on_exit_clicked(self):
        self.close()

    def update_current_time(self):
        """更新当前时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 0 in self.page_widgets:
            home_widget = self.page_widgets[0]
            home_widget.home_wg1_refleshtime_label.setText(f"数据更新时间：{current_time}")


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/home/home.ui", self)
        self.parent = parent

        # 初始化界面组件
        self.init_ui()
        self.init_time_filter()
        self.init_card_data()

        # 绑定信号
        self.home_wg1_refresh_toolButton.clicked.connect(self.refresh_data)

    def init_ui(self):
        """初始化界面布局"""
        # 设置表格属性
        self.init_goods_table()
        self.init_member_table()

        # 设置卡片样式
        self.set_card_styles()

        # 初始化时钟
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_current_time)
        self.time_timer.start(1000)

    def init_time_filter(self):
        """初始化时间筛选器"""
        self.home_wg1_date_comboBox.clear()
        time_ranges = [
            ("今天", 0),
            ("近3天", 3),
            ("近7天", 7),
            ("近30天", 30),
            ("近90天", 90)
        ]

        for text, days in time_ranges:
            self.home_wg1_date_comboBox.addItem(text, days)
        self.home_wg1_date_comboBox.setCurrentIndex(2)
        self.home_wg1_date_comboBox.currentIndexChanged.connect(self.update_all_data)

    def init_card_data(self):
        """初始化数据卡片"""
        # 固定数据
        self.home_wg2_gl_2_1_label1.setText(str(len(orders)))  # 总订单数
        self.home_wg2_gl_2_2_label1.setText(str(len(members)))  # 总会员数
        self.home_wg2_gl_2_3_label1.setText(str(len(goods)))  # 总商品数

        # 初始化动态数据
        self.update_card_data(7)

    def update_card_data(self, days):
        """更新动态卡片数据"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # 计算时间范围内的订单数据
        period_orders = []
        for o in orders:
            if o[11] is None:
                continue
            try:
                order_time = datetime.strptime(o[11], "%Y-%m-%d %H:%M:%S")
                if start_time <= order_time <= end_time:
                    period_orders.append(o)
            except (ValueError, TypeError):
                continue

        # 计算时间范围内的会员数据
        period_members = []
        for m in members:
            if m[12] is None:
                continue
            try:
                member_time = datetime.strptime(m[12], "%Y-%m-%d %H:%M:%S")
                if start_time <= member_time <= end_time:
                    period_members.append(m)
            except (ValueError, TypeError):
                continue

        # 计算时间范围内的商品数据
        period_goods = []
        for g in goods:
            if g[10] is None:
                continue
            try:
                goods_time = datetime.strptime(g[10], "%Y-%m-%d %H:%M:%S")
                if start_time <= goods_time <= end_time:
                    period_goods.append(g)
            except (ValueError, TypeError):
                continue

        # 更新动态数据
        self.home_wg2_gl_1_1_label1.setText(f"{sum(o[4] for o in period_orders):,.2f}")
        self.home_wg2_gl_1_2_label1.setText(str(len(period_members)))
        self.home_wg2_gl_1_3_label1.setText(str(len(period_goods)))

    def init_goods_table(self):
        """初始化商品表格"""
        table = self.home_wg5_wg_left_tableWidget
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['排行', '商品名称', '商品类别', '成交单数'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)

    def init_member_table(self):
        """初始化会员表格"""
        table = self.home_wg5_wg_right_tableWidget
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['排行', '会员名称', '消费笔数', '订单金额'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)

    def reload_data(self):
        """热重载时重新加载数据"""
        self.update_all_data()
        self.update_current_time()
        print("数据已热更新")

    def update_all_data(self):
        """更新所有数据"""
        days = self.home_wg1_date_comboBox.currentData()

        # 重新从数据文件加载数据
        import datas.orders as orders_module
        import datas.members as members_module
        import datas.goods as goods_module
        import datas.categories as categories_module
        importlib.reload(orders_module)
        importlib.reload(members_module)
        importlib.reload(goods_module)
        importlib.reload(categories_module)

        # 使用最新数据更新
        self.update_card_data(days)
        self.update_table_data(days)
        self.update_current_time()

    def update_table_data(self, days):
        # 获取当前时间范围
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # 重新加载数据模块
        from datas.orders import orders
        from datas.members import members
        from datas.goods import goods
        from datas.categories import categories

        # 商品数据处理
        goods_stats = {}
        for order in orders:
            try:
                # 跳过无效数据
                if not order[11] or not order[2] or not order[3]:
                    continue

                # 解析订单时间
                order_time = datetime.strptime(order[11], "%Y-%m-%d %H:%M:%S")

                # 时间范围过滤
                if start_time <= order_time <= end_time:
                    goods_id = order[2]
                    quantity = order[3]

                    # 关联商品数据
                    goods_item = next((g for g in goods if g[0] == goods_id), None)
                    if goods_item:
                        # 获取分类名称
                        category_id = goods_item[3]
                        category_name = next(
                            (cat[1] for cat in categories if cat[0] == category_id),
                            "未知分类"
                        )

                        # 统计商品销售数据
                        if goods_id not in goods_stats:
                            goods_stats[goods_id] = {
                                'name': goods_item[1],
                                'category': category_name,
                                'quantity': 0
                            }
                        goods_stats[goods_id]['quantity'] += quantity
            except (ValueError, TypeError, IndexError) as e:
                print(f"商品数据处理异常: {str(e)}")
                continue

        # 会员数据处理
        member_stats = {}
        for order in orders:
            try:
                # 跳过无效数据
                if not order[11] or not order[2]:
                    continue

                # 解析订单时间
                order_time = datetime.strptime(order[11], "%Y-%m-%d %H:%M:%S")

                # 时间范围过滤
                if start_time <= order_time <= end_time:
                    member_id = order[2]
                    amount = order[4]

                    # 关联会员数据
                    member_item = next((m for m in members if m[0] == member_id), None)
                    if member_item:
                        member_name = member_item[4] if len(member_item) > 4 else f"会员{member_id}"

                        # 统计会员消费数据
                        if member_id not in member_stats:
                            member_stats[member_id] = {
                                'name': member_name,
                                'orders': 0,
                                'amount': 0.0
                            }
                        member_stats[member_id]['orders'] += 1
                        member_stats[member_id]['amount'] += amount
            except (ValueError, TypeError, IndexError) as e:
                print(f"会员数据处理异常: {str(e)}")
                continue

        # 更新商品表格
        self.update_goods_table(goods_stats)
        # 更新会员表格
        self.update_member_table(member_stats)

    def update_goods_table(self, data):
        """更新商品销售表格"""
        table = self.home_wg5_wg_left_tableWidget
        table.setRowCount(0)

        # 按销量降序排序
        sorted_data = sorted(data.values(), key=lambda x: x['quantity'], reverse=True)[:15]

        # 设置行数
        table.setRowCount(len(sorted_data))

        # 填充数据（所有列居中）
        for row, item in enumerate(sorted_data):
            # 排行
            rank_item = QTableWidgetItem(f"No{row + 1}")
            rank_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, rank_item)

            # 商品名称
            name_item = QTableWidgetItem(item['name'])
            name_item.setToolTip(item['name'])
            name_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, name_item)

            # 商品分类
            category_item = QTableWidgetItem(item['category'])
            category_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, category_item)

            # 销售数量
            quantity_item = QTableWidgetItem(f"{item['quantity']:,}")
            quantity_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, quantity_item)

    def update_member_table(self, data):
        """更新会员消费表格"""
        table = self.home_wg5_wg_right_tableWidget
        table.setRowCount(0)

        # 按消费金额降序排序
        sorted_data = sorted(data.values(), key=lambda x: x['amount'], reverse=True)[:15]

        # 设置行数
        table.setRowCount(len(sorted_data))

        # 填充数据（所有列居中）
        for row, item in enumerate(sorted_data):
            # 排行
            rank_item = QTableWidgetItem(f"No{row + 1}")
            rank_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, rank_item)

            # 会员名称
            name_item = QTableWidgetItem(item['name'])
            name_item.setToolTip(item['name'])
            name_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, name_item)

            # 消费笔数
            orders_item = QTableWidgetItem(f"{item['orders']:,}")
            orders_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, orders_item)

            # 订单金额
            amount_item = QTableWidgetItem(f"¥{item['amount']:,.2f}")
            amount_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, amount_item)

    def refresh_data(self):
        """手动刷新数据"""
        self.update_all_data()
        self.update_current_time()
        print("数据已刷新")

    def update_current_time(self):
        """更新当前时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.home_wg1_refleshtime_label.setText(f"数据更新时间：{current_time}")

    def set_card_styles(self):
        """设置卡片样式"""
        value_labels = [
            self.home_wg2_gl_1_1_label1,
            self.home_wg2_gl_1_2_label1,
            self.home_wg2_gl_1_3_label1,
            self.home_wg2_gl_2_1_label1,
            self.home_wg2_gl_2_2_label1,
            self.home_wg2_gl_2_3_label1
        ]

        for label in value_labels:
            label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            label.setAlignment(Qt.AlignCenter)


class ManageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/manage/manage.ui", self)


class ChartsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/charts/charts.ui", self)


class RegDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/login/reg.ui", self)

    def open(self):
        self.show()