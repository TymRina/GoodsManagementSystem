# coding =utf-8
import math
import random

from PyQt5 import QtWidgets
import os
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QPen, QFont, QColor, QPainterPath, QImage, QBrush
from PyQt5.QtCore import Qt, QEasingCurve, QPointF
from PyQt5.QtChart import QScatterSeries, QHorizontalPercentBarSeries
from PyQt5.QtChart import (QChartView, QChart, QBarSeries, QBarSet, QLineSeries, QPieSeries,
                           QLegend, QBarCategoryAxis, QValueAxis)

current_dir = os.path.dirname(__file__)
ui_path = os.path.join(current_dir, "charts.ui")

page4_UI = uic.loadUiType(ui_path)[0]


class ChartsWidget(QtWidgets.QWidget, page4_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        '''
        初始化表单
        '''
        self.initChart_1_1()
        self.initChart_1_2()
        self.initChart_2_1()
        self.initChart_2_2()
        self.initChart_3_1()
        self.initChart_3_2()

    def initChart_1_1(self):
        '''
        创建第1行第1列的图表
        '''
        # 创建条状单元
        barSet0 = QBarSet('淘宝')
        barSet1 = QBarSet('拼多多')

        barSet0.append([1353, 6534, 7512, 7170, 3875, 4554])
        barSet1.append([1374, 2345, 5637, 3407, 8071, 6347])

        # 条状图
        barSeries = QBarSeries()
        barSeries.append(barSet0)
        barSeries.append(barSet1)

        # 创建图表
        chart = QChart()
        chart.addSeries(barSeries)
        chart.setTitle('多平台爆款销售情况')

        # 设置横向坐标(X轴)
        categories = ['一月', '二月', '三月', '四月', '五月', '六月']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        barSeries.attachAxis(axisX)

        axisX.setRange('一月', '六月')

        # 设置纵向坐标(Y轴)
        axisY = QValueAxis()
        axisY.setRange(1000, 9999)
        chart.addAxis(axisY, Qt.AlignLeft)
        barSeries.attachAxis(axisY)

        # 图例属性
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.p4_graphicsView_1_1 = QChartView(chart)
        self.p4_graphicsView_1_1.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_1_1.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_1_1.setObjectName("p4_graphicsView_1_1")
        self.p4_wg1_left_wg_ct_wg_hlayout.addWidget(self.p4_graphicsView_1_1)

    def initChart_1_2(self):
        '''
        创建第1行第2列的图表
        '''
        # 设置饼图数据
        pieSeries = QPieSeries()
        pieSeries.append('家具家电', 986)
        pieSeries.append('服装家居', 2853)
        pieSeries.append('房产汽车', 700)
        pieSeries.append('食品生鲜', 1335)
        pieSeries.append('母婴婴儿', 1256)

        # 处理索引号为1的片
        pieSlice = pieSeries.slices()[1]
        pieSlice.setExploded()
        pieSlice.setLabelVisible()  # 设置标签可见,缺省不可见
        pieSlice.setPen(QPen(Qt.darkGreen, 2))
        pieSlice.setBrush(Qt.green)

        # 创建图表
        chart2 = QChart()
        chart2.addSeries(pieSeries)
        chart2.setTitle('月销售类别')
        chart2.legend().setVisible(True)
        chart2.legend().setAlignment(Qt.AlignBottom)

        self.p4_graphicsView_1_2 = QChartView(chart2)
        self.p4_graphicsView_1_2.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_1_2.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_1_2.setObjectName("p4_graphicsView_1_2")
        self.p4_wg1_right_wg_ct_wg_hlayout.addWidget(self.p4_graphicsView_1_2)

    def initChart_2_1(self):
        '''
        创建第2行第1列的图表
        '''
        # 创建图表 并设置相关参数
        chart = QChart()
        chart.setTitle("日页面UV数(K)")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1000)
        chart.setAnimationEasingCurve(QEasingCurve.InOutCirc)
        chart.legend().show()

        # 创建折线数据序列
        lineSeries = QLineSeries()
        for value in range(0, 10):
            lineSeries.append(value, round(random.random() * 10, 2))

        lineSeries.setPointsVisible(True)
        lineSeries.setPointLabelsVisible(False)
        lineSeries.setPointLabelsFormat("(@xPoint, @yPoint)")
        lineSeries.setPointLabelsFont(QFont(None, 8))
        lineSeries.setPointLabelsColor(QColor(255, 0, 0))
        chart.addSeries(lineSeries)

        # 创建轴坐标
        # chart.createDefaultAxes()  # 创建默认轴
        axis_x = QValueAxis()
        axis_x.setLabelFormat("%d")
        axis_x.setTickCount(5)
        axis_x.setMinorTickCount(10)
        axis_x.setRange(0, 10)
        chart.addAxis(axis_x, Qt.AlignBottom)
        lineSeries.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        # axis_y.setTickType(QValueAxis.TicksDynamic)
        axis_y.setTickCount(5)
        axis_y.setMinorTickCount(3)
        axis_y.setRange(0, 10)
        chart.addAxis(axis_y, Qt.AlignLeft)
        lineSeries.attachAxis(axis_y)

        self.p4_graphicsView_2_1 = QChartView(chart)
        self.p4_graphicsView_2_1.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_2_1.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_2_1.setObjectName("p4_graphicsView_2_1")
        self.p4_wg3_left_wg_ct_wg_hlayout.addWidget(self.p4_graphicsView_2_1)

    def initChart_2_2(self):
        '''
        创建第2行第2列的图表
        '''
        chart = QChart()
        series = QLineSeries(chart)
        chart.setTheme(QChart.ChartThemeBrownSand)
        chart.setTitle("广东服装车间日生产数据")  # 设置图题
        chart.removeSeries(series)
        series.append(0, 6)
        series.append(1, 7)
        series.append(2, 4)
        series.setName('单井生产数据')  # 设置每条数据曲线的名称
        chart.addSeries(series)
        chart.createDefaultAxes()  # 创建默认轴
        chart.axisX().setTitleText('时间')  # 设置横坐标标题
        chart.axisY().setTitleText('产量')  # 设置横坐标标题

        self.p4_graphicsView_2_2 = QChartView(chart)
        self.p4_graphicsView_2_2.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_2_2.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_2_2.setObjectName("p4_graphicsView_2_2")
        self.p4_wg3_wg_right_ct_wg_hlayout.addWidget(self.p4_graphicsView_2_2)

    def initChart_3_1(self):
        '''
        创建第3行第1列的图表
        '''
        # 散点图
        scatterSeries0 = QScatterSeries()
        scatterSeries0.setName('电子产品')
        scatterSeries0.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        scatterSeries0.setMarkerSize(15.0)

        scatterSeries1 = QScatterSeries()
        scatterSeries1.setName('服装')
        scatterSeries1.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
        scatterSeries1.setMarkerSize(20.0)

        scatterSeries2 = QScatterSeries()
        scatterSeries2.setName('房产')
        scatterSeries2.setMarkerShape(QScatterSeries.MarkerShapeRectangle)
        scatterSeries2.setMarkerSize(30.0)

        scatterSeries0.append(0, 6)
        scatterSeries0.append(2, 4)
        scatterSeries0.append(3, 8)
        scatterSeries0.append(7, 9)
        scatterSeries0.append(10, 1)

        scatterSeries1 << QPointF(1, 1) << QPointF(3, 3) << QPointF(7, 6) << QPointF(8, 3) << QPointF(10, 2)
        scatterSeries2 << QPointF(1, 5) << QPointF(4, 6) << QPointF(6, 3) << QPointF(9, 5)

        starPath = QPainterPath()
        starPath.moveTo(28, 15)
        for i in range(1, 5):
            starPath.lineTo(14 + 14 * math.cos(0.8 * i * math.pi),
                            15 + 14 * math.sin(0.8 * i * math.pi))
        starPath.closeSubpath()

        star = QImage(30, 30, QImage.Format_ARGB32)
        star.fill(Qt.transparent)

        painter = QPainter(star)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0xf6a625))
        painter.setBrush(painter.pen().color())
        painter.drawPath(starPath)
        del painter

        scatterSeries2.setBrush(QBrush(star))
        scatterSeries2.setPen(QColor(Qt.transparent))

        # 创建图表
        chart = QChart()
        chart.addSeries(scatterSeries0)
        chart.addSeries(scatterSeries1)
        chart.addSeries(scatterSeries2)
        chart.setTitle('价格敏感探测')
        chart.createDefaultAxes()
        chart.setDropShadowEnabled(False)
        # 设置图例上标记形状
        chart.legend().setMarkerShape(QLegend.MarkerShapeFromSeries)

        # 图表视图
        self.p4_graphicsView_3_1 = QChartView(chart)
        self.p4_graphicsView_3_1.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_3_1.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_3_1.setObjectName("p4_graphicsView_3_1")
        self.p4_wg2_left_wg_ct_wg_hlayout.addWidget(self.p4_graphicsView_3_1)

    def initChart_3_2(self):
        '''
        创建第3行第2列的图表
        '''
        # 创建条状单元
        barSet0 = QBarSet('男装')
        barSet1 = QBarSet('婴儿')
        barSet2 = QBarSet('女装')
        barSet3 = QBarSet('家具')
        barSet4 = QBarSet('电子')

        barSet0.append([1, 2, 3, 4, 5, 6])
        barSet1.append([5, 0, 0, 4, 0, 7])
        barSet2.append([3, 5, 8, 13, 8, 5])
        barSet3.append([5, 6, 7, 3, 4, 5])
        barSet4.append([9, 7, 5, 3, 1, 2])

        # 条状图
        barSeries = QHorizontalPercentBarSeries()
        barSeries.append(barSet0)
        barSeries.append(barSet1)
        barSeries.append(barSet2)
        barSeries.append(barSet3)
        barSeries.append(barSet4)

        # 创建图表
        chart = QChart()
        chart.addSeries(barSeries)
        chart.setTitle('年度订单(万)')
        chart.setAnimationOptions(QChart.SeriesAnimations)  # 设置成动画显示

        # 设置横向坐标(X轴)
        categories = ['一月', '二月', '三月', '四月', '五月', '六月']
        axisY = QBarCategoryAxis()
        axisY.append(categories)
        chart.addAxis(axisY, Qt.AlignLeft)
        barSeries.attachAxis(axisY)

        # 设置纵向坐标(Y轴)
        axisX = QValueAxis()
        chart.addAxis(axisX, Qt.AlignBottom)
        barSeries.attachAxis(axisX)

        # 图例属性
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # 创建一个图表视图并设置图表
        self.p4_graphicsView_3_2 = QChartView(chart)
        self.p4_graphicsView_3_2.setRenderHint(QPainter.Antialiasing)
        self.p4_graphicsView_3_2.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.p4_graphicsView_3_2.setObjectName("p4_graphicsView_3_2")
        self.p4_wg2_wg_right_ct_wg_hlayout.addWidget(self.p4_graphicsView_3_2)
