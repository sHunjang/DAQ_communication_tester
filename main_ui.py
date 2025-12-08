# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(644, 741)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.com_group = QGroupBox(self.centralwidget)
        self.com_group.setObjectName(u"com_group")
        self.gridLayout_3 = QGridLayout(self.com_group)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.baudrate_combo = QComboBox(self.com_group)
        self.baudrate_combo.addItem("")
        self.baudrate_combo.addItem("")
        self.baudrate_combo.addItem("")
        self.baudrate_combo.addItem("")
        self.baudrate_combo.addItem("")
        self.baudrate_combo.setObjectName(u"baudrate_combo")
        self.baudrate_combo.setEditable(True)

        self.gridLayout_3.addWidget(self.baudrate_combo, 1, 1, 1, 1)

        self.label = QLabel(self.com_group)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.com_group)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.com_open_btn = QPushButton(self.com_group)
        self.com_open_btn.setObjectName(u"com_open_btn")

        self.gridLayout_3.addWidget(self.com_open_btn, 2, 0, 1, 1)

        self.com_close_btn = QPushButton(self.com_group)
        self.com_close_btn.setObjectName(u"com_close_btn")
        self.com_close_btn.setEnabled(False)

        self.gridLayout_3.addWidget(self.com_close_btn, 2, 1, 1, 1)

        self.com_combo = QComboBox(self.com_group)
        self.com_combo.setObjectName(u"com_combo")
        self.com_combo.setEditable(True)

        self.gridLayout_3.addWidget(self.com_combo, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.com_group, 0, 0, 1, 2)

        self.device_group = QGroupBox(self.centralwidget)
        self.device_group.setObjectName(u"device_group")
        self.gridLayout_15 = QGridLayout(self.device_group)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.device_tab = QTabWidget(self.device_group)
        self.device_tab.setObjectName(u"device_tab")
        font = QFont()
        font.setPointSize(9)
        self.device_tab.setFont(font)
        self.tag1p2w_tab = QWidget()
        self.tag1p2w_tab.setObjectName(u"tag1p2w_tab")
        self.gridLayout_16 = QGridLayout(self.tag1p2w_tab)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.tag1p2w_7_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_7_group.setObjectName(u"tag1p2w_7_group")
        self.tag1p2w_7_group.setCheckable(True)
        self.verticalLayout_98 = QVBoxLayout(self.tag1p2w_7_group)
        self.verticalLayout_98.setObjectName(u"verticalLayout_98")
        self.tag1p2w_7_normal_radio = QRadioButton(self.tag1p2w_7_group)
        self.tag1p2w_7_normal_radio.setObjectName(u"tag1p2w_7_normal_radio")
        self.tag1p2w_7_normal_radio.setChecked(True)

        self.verticalLayout_98.addWidget(self.tag1p2w_7_normal_radio)

        self.tag1p2w_7_crc_radio = QRadioButton(self.tag1p2w_7_group)
        self.tag1p2w_7_crc_radio.setObjectName(u"tag1p2w_7_crc_radio")

        self.verticalLayout_98.addWidget(self.tag1p2w_7_crc_radio)

        self.tag1p2w_7_timing_radio = QRadioButton(self.tag1p2w_7_group)
        self.tag1p2w_7_timing_radio.setObjectName(u"tag1p2w_7_timing_radio")

        self.verticalLayout_98.addWidget(self.tag1p2w_7_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_7_group, 1, 2, 1, 1)

        self.tag1p2w_5_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_5_group.setObjectName(u"tag1p2w_5_group")
        self.tag1p2w_5_group.setCheckable(True)
        self.verticalLayout_96 = QVBoxLayout(self.tag1p2w_5_group)
        self.verticalLayout_96.setObjectName(u"verticalLayout_96")
        self.tag1p2w_5_normal_radio = QRadioButton(self.tag1p2w_5_group)
        self.tag1p2w_5_normal_radio.setObjectName(u"tag1p2w_5_normal_radio")
        self.tag1p2w_5_normal_radio.setChecked(True)

        self.verticalLayout_96.addWidget(self.tag1p2w_5_normal_radio)

        self.tag1p2w_5_crc_radio = QRadioButton(self.tag1p2w_5_group)
        self.tag1p2w_5_crc_radio.setObjectName(u"tag1p2w_5_crc_radio")

        self.verticalLayout_96.addWidget(self.tag1p2w_5_crc_radio)

        self.tag1p2w_5_timing_radio = QRadioButton(self.tag1p2w_5_group)
        self.tag1p2w_5_timing_radio.setObjectName(u"tag1p2w_5_timing_radio")

        self.verticalLayout_96.addWidget(self.tag1p2w_5_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_5_group, 1, 0, 1, 1)

        self.tag1p2w_8_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_8_group.setObjectName(u"tag1p2w_8_group")
        self.tag1p2w_8_group.setCheckable(True)
        self.verticalLayout_99 = QVBoxLayout(self.tag1p2w_8_group)
        self.verticalLayout_99.setObjectName(u"verticalLayout_99")
        self.tag1p2w_8_normal_radio = QRadioButton(self.tag1p2w_8_group)
        self.tag1p2w_8_normal_radio.setObjectName(u"tag1p2w_8_normal_radio")
        self.tag1p2w_8_normal_radio.setChecked(True)

        self.verticalLayout_99.addWidget(self.tag1p2w_8_normal_radio)

        self.tag1p2w_8_crc_radio = QRadioButton(self.tag1p2w_8_group)
        self.tag1p2w_8_crc_radio.setObjectName(u"tag1p2w_8_crc_radio")

        self.verticalLayout_99.addWidget(self.tag1p2w_8_crc_radio)

        self.tag1p2w_8_timing_radio = QRadioButton(self.tag1p2w_8_group)
        self.tag1p2w_8_timing_radio.setObjectName(u"tag1p2w_8_timing_radio")

        self.verticalLayout_99.addWidget(self.tag1p2w_8_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_8_group, 1, 3, 1, 1)

        self.tag1p2w_6_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_6_group.setObjectName(u"tag1p2w_6_group")
        self.tag1p2w_6_group.setCheckable(True)
        self.verticalLayout_97 = QVBoxLayout(self.tag1p2w_6_group)
        self.verticalLayout_97.setObjectName(u"verticalLayout_97")
        self.tag1p2w_6_normal_radio = QRadioButton(self.tag1p2w_6_group)
        self.tag1p2w_6_normal_radio.setObjectName(u"tag1p2w_6_normal_radio")
        self.tag1p2w_6_normal_radio.setChecked(True)

        self.verticalLayout_97.addWidget(self.tag1p2w_6_normal_radio)

        self.tag1p2w_6_crc_radio = QRadioButton(self.tag1p2w_6_group)
        self.tag1p2w_6_crc_radio.setObjectName(u"tag1p2w_6_crc_radio")

        self.verticalLayout_97.addWidget(self.tag1p2w_6_crc_radio)

        self.tag1p2w_6_timing_radio = QRadioButton(self.tag1p2w_6_group)
        self.tag1p2w_6_timing_radio.setObjectName(u"tag1p2w_6_timing_radio")

        self.verticalLayout_97.addWidget(self.tag1p2w_6_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_6_group, 1, 1, 1, 1)

        self.tag1p2w_4_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_4_group.setObjectName(u"tag1p2w_4_group")
        self.tag1p2w_4_group.setCheckable(True)
        self.verticalLayout_95 = QVBoxLayout(self.tag1p2w_4_group)
        self.verticalLayout_95.setObjectName(u"verticalLayout_95")
        self.tag1p2w_4_normal_radio = QRadioButton(self.tag1p2w_4_group)
        self.tag1p2w_4_normal_radio.setObjectName(u"tag1p2w_4_normal_radio")
        self.tag1p2w_4_normal_radio.setChecked(True)

        self.verticalLayout_95.addWidget(self.tag1p2w_4_normal_radio)

        self.tag1p2w_4_crc_radio = QRadioButton(self.tag1p2w_4_group)
        self.tag1p2w_4_crc_radio.setObjectName(u"tag1p2w_4_crc_radio")

        self.verticalLayout_95.addWidget(self.tag1p2w_4_crc_radio)

        self.tag1p2w_4_timing_radio = QRadioButton(self.tag1p2w_4_group)
        self.tag1p2w_4_timing_radio.setObjectName(u"tag1p2w_4_timing_radio")

        self.verticalLayout_95.addWidget(self.tag1p2w_4_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_4_group, 0, 4, 1, 1)

        self.tag1p2w_2_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_2_group.setObjectName(u"tag1p2w_2_group")
        self.tag1p2w_2_group.setCheckable(True)
        self.verticalLayout_93 = QVBoxLayout(self.tag1p2w_2_group)
        self.verticalLayout_93.setObjectName(u"verticalLayout_93")
        self.tag1p2w_2_normal_radio = QRadioButton(self.tag1p2w_2_group)
        self.tag1p2w_2_normal_radio.setObjectName(u"tag1p2w_2_normal_radio")
        self.tag1p2w_2_normal_radio.setChecked(True)

        self.verticalLayout_93.addWidget(self.tag1p2w_2_normal_radio)

        self.tag1p2w_2_crc_radio = QRadioButton(self.tag1p2w_2_group)
        self.tag1p2w_2_crc_radio.setObjectName(u"tag1p2w_2_crc_radio")

        self.verticalLayout_93.addWidget(self.tag1p2w_2_crc_radio)

        self.tag1p2w_2_timing_radio = QRadioButton(self.tag1p2w_2_group)
        self.tag1p2w_2_timing_radio.setObjectName(u"tag1p2w_2_timing_radio")

        self.verticalLayout_93.addWidget(self.tag1p2w_2_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_2_group, 0, 2, 1, 1)

        self.tag1p2w_9_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_9_group.setObjectName(u"tag1p2w_9_group")
        self.tag1p2w_9_group.setCheckable(True)
        self.tag1p2w_9_group.setChecked(True)
        self.verticalLayout_100 = QVBoxLayout(self.tag1p2w_9_group)
        self.verticalLayout_100.setObjectName(u"verticalLayout_100")
        self.tag1p2w_9_normal_radio = QRadioButton(self.tag1p2w_9_group)
        self.tag1p2w_9_normal_radio.setObjectName(u"tag1p2w_9_normal_radio")
        self.tag1p2w_9_normal_radio.setChecked(True)

        self.verticalLayout_100.addWidget(self.tag1p2w_9_normal_radio)

        self.tag1p2w_9_crc_radio = QRadioButton(self.tag1p2w_9_group)
        self.tag1p2w_9_crc_radio.setObjectName(u"tag1p2w_9_crc_radio")

        self.verticalLayout_100.addWidget(self.tag1p2w_9_crc_radio)

        self.tag1p2w_9_timing_radio = QRadioButton(self.tag1p2w_9_group)
        self.tag1p2w_9_timing_radio.setObjectName(u"tag1p2w_9_timing_radio")

        self.verticalLayout_100.addWidget(self.tag1p2w_9_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_9_group, 1, 4, 1, 1)

        self.tag1p2w_0_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_0_group.setObjectName(u"tag1p2w_0_group")
        self.tag1p2w_0_group.setCheckable(True)
        self.verticalLayout_91 = QVBoxLayout(self.tag1p2w_0_group)
        self.verticalLayout_91.setObjectName(u"verticalLayout_91")
        self.tag1p2w_0_normal_radio = QRadioButton(self.tag1p2w_0_group)
        self.tag1p2w_0_normal_radio.setObjectName(u"tag1p2w_0_normal_radio")
        self.tag1p2w_0_normal_radio.setChecked(True)

        self.verticalLayout_91.addWidget(self.tag1p2w_0_normal_radio)

        self.tag1p2w_0_crc_radio = QRadioButton(self.tag1p2w_0_group)
        self.tag1p2w_0_crc_radio.setObjectName(u"tag1p2w_0_crc_radio")

        self.verticalLayout_91.addWidget(self.tag1p2w_0_crc_radio)

        self.tag1p2w_0_timing_radio = QRadioButton(self.tag1p2w_0_group)
        self.tag1p2w_0_timing_radio.setObjectName(u"tag1p2w_0_timing_radio")

        self.verticalLayout_91.addWidget(self.tag1p2w_0_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_0_group, 0, 0, 1, 1)

        self.tag1p2w_3_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_3_group.setObjectName(u"tag1p2w_3_group")
        self.tag1p2w_3_group.setCheckable(True)
        self.verticalLayout_94 = QVBoxLayout(self.tag1p2w_3_group)
        self.verticalLayout_94.setObjectName(u"verticalLayout_94")
        self.tag1p2w_3_normal_radio = QRadioButton(self.tag1p2w_3_group)
        self.tag1p2w_3_normal_radio.setObjectName(u"tag1p2w_3_normal_radio")
        self.tag1p2w_3_normal_radio.setChecked(True)

        self.verticalLayout_94.addWidget(self.tag1p2w_3_normal_radio)

        self.tag1p2w_3_crc_radio = QRadioButton(self.tag1p2w_3_group)
        self.tag1p2w_3_crc_radio.setObjectName(u"tag1p2w_3_crc_radio")

        self.verticalLayout_94.addWidget(self.tag1p2w_3_crc_radio)

        self.tag1p2w_3_timing_radio = QRadioButton(self.tag1p2w_3_group)
        self.tag1p2w_3_timing_radio.setObjectName(u"tag1p2w_3_timing_radio")

        self.verticalLayout_94.addWidget(self.tag1p2w_3_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_3_group, 0, 3, 1, 1)

        self.tag1p2w_1_group = QGroupBox(self.tag1p2w_tab)
        self.tag1p2w_1_group.setObjectName(u"tag1p2w_1_group")
        self.tag1p2w_1_group.setFlat(False)
        self.tag1p2w_1_group.setCheckable(True)
        self.verticalLayout_92 = QVBoxLayout(self.tag1p2w_1_group)
        self.verticalLayout_92.setObjectName(u"verticalLayout_92")
        self.tag1p2w_1_normal_radio = QRadioButton(self.tag1p2w_1_group)
        self.tag1p2w_1_normal_radio.setObjectName(u"tag1p2w_1_normal_radio")
        self.tag1p2w_1_normal_radio.setChecked(True)

        self.verticalLayout_92.addWidget(self.tag1p2w_1_normal_radio)

        self.tag1p2w_1_crc_radio = QRadioButton(self.tag1p2w_1_group)
        self.tag1p2w_1_crc_radio.setObjectName(u"tag1p2w_1_crc_radio")

        self.verticalLayout_92.addWidget(self.tag1p2w_1_crc_radio)

        self.tag1p2w_1_timing_radio = QRadioButton(self.tag1p2w_1_group)
        self.tag1p2w_1_timing_radio.setObjectName(u"tag1p2w_1_timing_radio")

        self.verticalLayout_92.addWidget(self.tag1p2w_1_timing_radio)


        self.gridLayout_16.addWidget(self.tag1p2w_1_group, 0, 1, 1, 1)

        self.device_tab.addTab(self.tag1p2w_tab, "")
        self.tag3p3w_tab = QWidget()
        self.tag3p3w_tab.setObjectName(u"tag3p3w_tab")
        self.gridLayout_17 = QGridLayout(self.tag3p3w_tab)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.tag3p3w_0_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_0_group.setObjectName(u"tag3p3w_0_group")
        self.tag3p3w_0_group.setCheckable(True)
        self.verticalLayout_101 = QVBoxLayout(self.tag3p3w_0_group)
        self.verticalLayout_101.setObjectName(u"verticalLayout_101")
        self.tag3p3w_0_normal_radio = QRadioButton(self.tag3p3w_0_group)
        self.tag3p3w_0_normal_radio.setObjectName(u"tag3p3w_0_normal_radio")
        self.tag3p3w_0_normal_radio.setChecked(True)

        self.verticalLayout_101.addWidget(self.tag3p3w_0_normal_radio)

        self.tag3p3w_0_crc_radio = QRadioButton(self.tag3p3w_0_group)
        self.tag3p3w_0_crc_radio.setObjectName(u"tag3p3w_0_crc_radio")

        self.verticalLayout_101.addWidget(self.tag3p3w_0_crc_radio)

        self.tag3p3w_0_timing_radio = QRadioButton(self.tag3p3w_0_group)
        self.tag3p3w_0_timing_radio.setObjectName(u"tag3p3w_0_timing_radio")

        self.verticalLayout_101.addWidget(self.tag3p3w_0_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_0_group, 0, 0, 1, 1)

        self.tag3p3w_1_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_1_group.setObjectName(u"tag3p3w_1_group")
        self.tag3p3w_1_group.setCheckable(True)
        self.verticalLayout_102 = QVBoxLayout(self.tag3p3w_1_group)
        self.verticalLayout_102.setObjectName(u"verticalLayout_102")
        self.tag3p3w_1_normal_radio = QRadioButton(self.tag3p3w_1_group)
        self.tag3p3w_1_normal_radio.setObjectName(u"tag3p3w_1_normal_radio")
        self.tag3p3w_1_normal_radio.setChecked(True)

        self.verticalLayout_102.addWidget(self.tag3p3w_1_normal_radio)

        self.tag3p3w_1_crc_radio = QRadioButton(self.tag3p3w_1_group)
        self.tag3p3w_1_crc_radio.setObjectName(u"tag3p3w_1_crc_radio")

        self.verticalLayout_102.addWidget(self.tag3p3w_1_crc_radio)

        self.tag3p3w_1_timing_radio = QRadioButton(self.tag3p3w_1_group)
        self.tag3p3w_1_timing_radio.setObjectName(u"tag3p3w_1_timing_radio")

        self.verticalLayout_102.addWidget(self.tag3p3w_1_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_1_group, 0, 1, 1, 1)

        self.tag3p3w_2_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_2_group.setObjectName(u"tag3p3w_2_group")
        self.tag3p3w_2_group.setCheckable(True)
        self.verticalLayout_103 = QVBoxLayout(self.tag3p3w_2_group)
        self.verticalLayout_103.setObjectName(u"verticalLayout_103")
        self.tag3p3w_2_normal_radio = QRadioButton(self.tag3p3w_2_group)
        self.tag3p3w_2_normal_radio.setObjectName(u"tag3p3w_2_normal_radio")
        self.tag3p3w_2_normal_radio.setChecked(True)

        self.verticalLayout_103.addWidget(self.tag3p3w_2_normal_radio)

        self.tag3p3w_2_crc_radio = QRadioButton(self.tag3p3w_2_group)
        self.tag3p3w_2_crc_radio.setObjectName(u"tag3p3w_2_crc_radio")

        self.verticalLayout_103.addWidget(self.tag3p3w_2_crc_radio)

        self.tag3p3w_2_timing_radio = QRadioButton(self.tag3p3w_2_group)
        self.tag3p3w_2_timing_radio.setObjectName(u"tag3p3w_2_timing_radio")

        self.verticalLayout_103.addWidget(self.tag3p3w_2_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_2_group, 0, 2, 1, 1)

        self.tag3p3w_3_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_3_group.setObjectName(u"tag3p3w_3_group")
        self.tag3p3w_3_group.setCheckable(True)
        self.verticalLayout_104 = QVBoxLayout(self.tag3p3w_3_group)
        self.verticalLayout_104.setObjectName(u"verticalLayout_104")
        self.tag3p3w_3_normal_radio = QRadioButton(self.tag3p3w_3_group)
        self.tag3p3w_3_normal_radio.setObjectName(u"tag3p3w_3_normal_radio")
        self.tag3p3w_3_normal_radio.setChecked(True)

        self.verticalLayout_104.addWidget(self.tag3p3w_3_normal_radio)

        self.tag3p3w_3_crc_radio = QRadioButton(self.tag3p3w_3_group)
        self.tag3p3w_3_crc_radio.setObjectName(u"tag3p3w_3_crc_radio")

        self.verticalLayout_104.addWidget(self.tag3p3w_3_crc_radio)

        self.tag3p3w_3_timing_radio = QRadioButton(self.tag3p3w_3_group)
        self.tag3p3w_3_timing_radio.setObjectName(u"tag3p3w_3_timing_radio")

        self.verticalLayout_104.addWidget(self.tag3p3w_3_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_3_group, 0, 3, 1, 1)

        self.tag3p3w_4_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_4_group.setObjectName(u"tag3p3w_4_group")
        self.tag3p3w_4_group.setCheckable(True)
        self.verticalLayout_105 = QVBoxLayout(self.tag3p3w_4_group)
        self.verticalLayout_105.setObjectName(u"verticalLayout_105")
        self.tag3p3w_4_normal_radio = QRadioButton(self.tag3p3w_4_group)
        self.tag3p3w_4_normal_radio.setObjectName(u"tag3p3w_4_normal_radio")
        self.tag3p3w_4_normal_radio.setChecked(True)

        self.verticalLayout_105.addWidget(self.tag3p3w_4_normal_radio)

        self.tag3p3w_4_crc_radio = QRadioButton(self.tag3p3w_4_group)
        self.tag3p3w_4_crc_radio.setObjectName(u"tag3p3w_4_crc_radio")

        self.verticalLayout_105.addWidget(self.tag3p3w_4_crc_radio)

        self.tag3p3w_4_timing_radio = QRadioButton(self.tag3p3w_4_group)
        self.tag3p3w_4_timing_radio.setObjectName(u"tag3p3w_4_timing_radio")

        self.verticalLayout_105.addWidget(self.tag3p3w_4_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_4_group, 0, 4, 1, 1)

        self.tag3p3w_5_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_5_group.setObjectName(u"tag3p3w_5_group")
        self.tag3p3w_5_group.setCheckable(True)
        self.verticalLayout_106 = QVBoxLayout(self.tag3p3w_5_group)
        self.verticalLayout_106.setObjectName(u"verticalLayout_106")
        self.tag3p3w_5_normal_radio = QRadioButton(self.tag3p3w_5_group)
        self.tag3p3w_5_normal_radio.setObjectName(u"tag3p3w_5_normal_radio")
        self.tag3p3w_5_normal_radio.setChecked(True)

        self.verticalLayout_106.addWidget(self.tag3p3w_5_normal_radio)

        self.tag3p3w_5_crc_radio = QRadioButton(self.tag3p3w_5_group)
        self.tag3p3w_5_crc_radio.setObjectName(u"tag3p3w_5_crc_radio")

        self.verticalLayout_106.addWidget(self.tag3p3w_5_crc_radio)

        self.tag3p3w_5_timing_radio = QRadioButton(self.tag3p3w_5_group)
        self.tag3p3w_5_timing_radio.setObjectName(u"tag3p3w_5_timing_radio")

        self.verticalLayout_106.addWidget(self.tag3p3w_5_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_5_group, 1, 0, 1, 1)

        self.tag3p3w_6_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_6_group.setObjectName(u"tag3p3w_6_group")
        self.tag3p3w_6_group.setCheckable(True)
        self.verticalLayout_107 = QVBoxLayout(self.tag3p3w_6_group)
        self.verticalLayout_107.setObjectName(u"verticalLayout_107")
        self.tag3p3w_6_normal_radio = QRadioButton(self.tag3p3w_6_group)
        self.tag3p3w_6_normal_radio.setObjectName(u"tag3p3w_6_normal_radio")
        self.tag3p3w_6_normal_radio.setChecked(True)

        self.verticalLayout_107.addWidget(self.tag3p3w_6_normal_radio)

        self.tag3p3w_6_crc_radio = QRadioButton(self.tag3p3w_6_group)
        self.tag3p3w_6_crc_radio.setObjectName(u"tag3p3w_6_crc_radio")

        self.verticalLayout_107.addWidget(self.tag3p3w_6_crc_radio)

        self.tag3p3w_6_timing_radio = QRadioButton(self.tag3p3w_6_group)
        self.tag3p3w_6_timing_radio.setObjectName(u"tag3p3w_6_timing_radio")

        self.verticalLayout_107.addWidget(self.tag3p3w_6_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_6_group, 1, 1, 1, 1)

        self.tag3p3w_7_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_7_group.setObjectName(u"tag3p3w_7_group")
        self.tag3p3w_7_group.setCheckable(True)
        self.verticalLayout_108 = QVBoxLayout(self.tag3p3w_7_group)
        self.verticalLayout_108.setObjectName(u"verticalLayout_108")
        self.tag3p3w_7_normal_radio = QRadioButton(self.tag3p3w_7_group)
        self.tag3p3w_7_normal_radio.setObjectName(u"tag3p3w_7_normal_radio")
        self.tag3p3w_7_normal_radio.setChecked(True)

        self.verticalLayout_108.addWidget(self.tag3p3w_7_normal_radio)

        self.tag3p3w_7_crc_radio = QRadioButton(self.tag3p3w_7_group)
        self.tag3p3w_7_crc_radio.setObjectName(u"tag3p3w_7_crc_radio")

        self.verticalLayout_108.addWidget(self.tag3p3w_7_crc_radio)

        self.tag3p3w_7_timing_radio = QRadioButton(self.tag3p3w_7_group)
        self.tag3p3w_7_timing_radio.setObjectName(u"tag3p3w_7_timing_radio")

        self.verticalLayout_108.addWidget(self.tag3p3w_7_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_7_group, 1, 2, 1, 1)

        self.tag3p3w_8_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_8_group.setObjectName(u"tag3p3w_8_group")
        self.tag3p3w_8_group.setCheckable(True)
        self.verticalLayout_109 = QVBoxLayout(self.tag3p3w_8_group)
        self.verticalLayout_109.setObjectName(u"verticalLayout_109")
        self.tag3p3w_8_normal_radio = QRadioButton(self.tag3p3w_8_group)
        self.tag3p3w_8_normal_radio.setObjectName(u"tag3p3w_8_normal_radio")
        self.tag3p3w_8_normal_radio.setChecked(True)

        self.verticalLayout_109.addWidget(self.tag3p3w_8_normal_radio)

        self.tag3p3w_8_crc_radio = QRadioButton(self.tag3p3w_8_group)
        self.tag3p3w_8_crc_radio.setObjectName(u"tag3p3w_8_crc_radio")

        self.verticalLayout_109.addWidget(self.tag3p3w_8_crc_radio)

        self.tag3p3w_8_timing_radio = QRadioButton(self.tag3p3w_8_group)
        self.tag3p3w_8_timing_radio.setObjectName(u"tag3p3w_8_timing_radio")

        self.verticalLayout_109.addWidget(self.tag3p3w_8_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_8_group, 1, 3, 1, 1)

        self.tag3p3w_9_group = QGroupBox(self.tag3p3w_tab)
        self.tag3p3w_9_group.setObjectName(u"tag3p3w_9_group")
        self.tag3p3w_9_group.setCheckable(True)
        self.verticalLayout_110 = QVBoxLayout(self.tag3p3w_9_group)
        self.verticalLayout_110.setObjectName(u"verticalLayout_110")
        self.tag3p3w_9_normal_radio = QRadioButton(self.tag3p3w_9_group)
        self.tag3p3w_9_normal_radio.setObjectName(u"tag3p3w_9_normal_radio")
        self.tag3p3w_9_normal_radio.setChecked(True)

        self.verticalLayout_110.addWidget(self.tag3p3w_9_normal_radio)

        self.tag3p3w_9_crc_radio = QRadioButton(self.tag3p3w_9_group)
        self.tag3p3w_9_crc_radio.setObjectName(u"tag3p3w_9_crc_radio")

        self.verticalLayout_110.addWidget(self.tag3p3w_9_crc_radio)

        self.tag3p3w_9_timing_radio = QRadioButton(self.tag3p3w_9_group)
        self.tag3p3w_9_timing_radio.setObjectName(u"tag3p3w_9_timing_radio")

        self.verticalLayout_110.addWidget(self.tag3p3w_9_timing_radio)


        self.gridLayout_17.addWidget(self.tag3p3w_9_group, 1, 4, 1, 1)

        self.device_tab.addTab(self.tag3p3w_tab, "")
        self.tag3p4w_tab = QWidget()
        self.tag3p4w_tab.setObjectName(u"tag3p4w_tab")
        self.gridLayout_18 = QGridLayout(self.tag3p4w_tab)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.tag3p4w_0_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_0_group.setObjectName(u"tag3p4w_0_group")
        self.tag3p4w_0_group.setCheckable(True)
        self.verticalLayout_111 = QVBoxLayout(self.tag3p4w_0_group)
        self.verticalLayout_111.setObjectName(u"verticalLayout_111")
        self.tag3p4w_0_normal_radio = QRadioButton(self.tag3p4w_0_group)
        self.tag3p4w_0_normal_radio.setObjectName(u"tag3p4w_0_normal_radio")
        self.tag3p4w_0_normal_radio.setChecked(True)

        self.verticalLayout_111.addWidget(self.tag3p4w_0_normal_radio)

        self.tag3p4w_0_crc_radio = QRadioButton(self.tag3p4w_0_group)
        self.tag3p4w_0_crc_radio.setObjectName(u"tag3p4w_0_crc_radio")

        self.verticalLayout_111.addWidget(self.tag3p4w_0_crc_radio)

        self.tag3p4w_0_timing_radio = QRadioButton(self.tag3p4w_0_group)
        self.tag3p4w_0_timing_radio.setObjectName(u"tag3p4w_0_timing_radio")

        self.verticalLayout_111.addWidget(self.tag3p4w_0_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_0_group, 0, 0, 1, 1)

        self.tag3p4w_1_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_1_group.setObjectName(u"tag3p4w_1_group")
        self.tag3p4w_1_group.setCheckable(True)
        self.verticalLayout_112 = QVBoxLayout(self.tag3p4w_1_group)
        self.verticalLayout_112.setObjectName(u"verticalLayout_112")
        self.tag3p4w_1_normal_radio = QRadioButton(self.tag3p4w_1_group)
        self.tag3p4w_1_normal_radio.setObjectName(u"tag3p4w_1_normal_radio")
        self.tag3p4w_1_normal_radio.setChecked(True)

        self.verticalLayout_112.addWidget(self.tag3p4w_1_normal_radio)

        self.tag3p4w_1_crc_radio = QRadioButton(self.tag3p4w_1_group)
        self.tag3p4w_1_crc_radio.setObjectName(u"tag3p4w_1_crc_radio")

        self.verticalLayout_112.addWidget(self.tag3p4w_1_crc_radio)

        self.tag3p4w_1_timing_radio = QRadioButton(self.tag3p4w_1_group)
        self.tag3p4w_1_timing_radio.setObjectName(u"tag3p4w_1_timing_radio")

        self.verticalLayout_112.addWidget(self.tag3p4w_1_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_1_group, 0, 1, 1, 1)

        self.tag3p4w_2_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_2_group.setObjectName(u"tag3p4w_2_group")
        self.tag3p4w_2_group.setCheckable(True)
        self.verticalLayout_113 = QVBoxLayout(self.tag3p4w_2_group)
        self.verticalLayout_113.setObjectName(u"verticalLayout_113")
        self.tag3p4w_2_normal_radio = QRadioButton(self.tag3p4w_2_group)
        self.tag3p4w_2_normal_radio.setObjectName(u"tag3p4w_2_normal_radio")
        self.tag3p4w_2_normal_radio.setChecked(True)

        self.verticalLayout_113.addWidget(self.tag3p4w_2_normal_radio)

        self.tag3p4w_2_crc_radio = QRadioButton(self.tag3p4w_2_group)
        self.tag3p4w_2_crc_radio.setObjectName(u"tag3p4w_2_crc_radio")

        self.verticalLayout_113.addWidget(self.tag3p4w_2_crc_radio)

        self.tag3p4w_2_timing_radio = QRadioButton(self.tag3p4w_2_group)
        self.tag3p4w_2_timing_radio.setObjectName(u"tag3p4w_2_timing_radio")

        self.verticalLayout_113.addWidget(self.tag3p4w_2_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_2_group, 0, 2, 1, 1)

        self.tag3p4w_3_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_3_group.setObjectName(u"tag3p4w_3_group")
        self.tag3p4w_3_group.setCheckable(True)
        self.verticalLayout_114 = QVBoxLayout(self.tag3p4w_3_group)
        self.verticalLayout_114.setObjectName(u"verticalLayout_114")
        self.tag3p4w_3_normal_radio = QRadioButton(self.tag3p4w_3_group)
        self.tag3p4w_3_normal_radio.setObjectName(u"tag3p4w_3_normal_radio")
        self.tag3p4w_3_normal_radio.setChecked(True)

        self.verticalLayout_114.addWidget(self.tag3p4w_3_normal_radio)

        self.tag3p4w_3_crc_radio = QRadioButton(self.tag3p4w_3_group)
        self.tag3p4w_3_crc_radio.setObjectName(u"tag3p4w_3_crc_radio")

        self.verticalLayout_114.addWidget(self.tag3p4w_3_crc_radio)

        self.tag3p4w_3_timing_radio = QRadioButton(self.tag3p4w_3_group)
        self.tag3p4w_3_timing_radio.setObjectName(u"tag3p4w_3_timing_radio")

        self.verticalLayout_114.addWidget(self.tag3p4w_3_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_3_group, 0, 3, 1, 1)

        self.tag3p4w_4_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_4_group.setObjectName(u"tag3p4w_4_group")
        self.tag3p4w_4_group.setCheckable(True)
        self.verticalLayout_115 = QVBoxLayout(self.tag3p4w_4_group)
        self.verticalLayout_115.setObjectName(u"verticalLayout_115")
        self.tag3p4w_4_normal_radio = QRadioButton(self.tag3p4w_4_group)
        self.tag3p4w_4_normal_radio.setObjectName(u"tag3p4w_4_normal_radio")
        self.tag3p4w_4_normal_radio.setChecked(True)

        self.verticalLayout_115.addWidget(self.tag3p4w_4_normal_radio)

        self.tag3p4w_4_crc_radio = QRadioButton(self.tag3p4w_4_group)
        self.tag3p4w_4_crc_radio.setObjectName(u"tag3p4w_4_crc_radio")

        self.verticalLayout_115.addWidget(self.tag3p4w_4_crc_radio)

        self.tag3p4w_4_timing_radio = QRadioButton(self.tag3p4w_4_group)
        self.tag3p4w_4_timing_radio.setObjectName(u"tag3p4w_4_timing_radio")

        self.verticalLayout_115.addWidget(self.tag3p4w_4_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_4_group, 0, 4, 1, 1)

        self.tag3p4w_5_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_5_group.setObjectName(u"tag3p4w_5_group")
        self.tag3p4w_5_group.setCheckable(True)
        self.verticalLayout_116 = QVBoxLayout(self.tag3p4w_5_group)
        self.verticalLayout_116.setObjectName(u"verticalLayout_116")
        self.tag3p4w_5_normal_radio = QRadioButton(self.tag3p4w_5_group)
        self.tag3p4w_5_normal_radio.setObjectName(u"tag3p4w_5_normal_radio")
        self.tag3p4w_5_normal_radio.setChecked(True)

        self.verticalLayout_116.addWidget(self.tag3p4w_5_normal_radio)

        self.tag3p4w_5_crc_radio = QRadioButton(self.tag3p4w_5_group)
        self.tag3p4w_5_crc_radio.setObjectName(u"tag3p4w_5_crc_radio")

        self.verticalLayout_116.addWidget(self.tag3p4w_5_crc_radio)

        self.tag3p4w_5_timing_radio = QRadioButton(self.tag3p4w_5_group)
        self.tag3p4w_5_timing_radio.setObjectName(u"tag3p4w_5_timing_radio")

        self.verticalLayout_116.addWidget(self.tag3p4w_5_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_5_group, 1, 0, 1, 1)

        self.tag3p4w_6_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_6_group.setObjectName(u"tag3p4w_6_group")
        self.tag3p4w_6_group.setCheckable(True)
        self.verticalLayout_117 = QVBoxLayout(self.tag3p4w_6_group)
        self.verticalLayout_117.setObjectName(u"verticalLayout_117")
        self.tag3p4w_6_normal_radio = QRadioButton(self.tag3p4w_6_group)
        self.tag3p4w_6_normal_radio.setObjectName(u"tag3p4w_6_normal_radio")
        self.tag3p4w_6_normal_radio.setChecked(True)

        self.verticalLayout_117.addWidget(self.tag3p4w_6_normal_radio)

        self.tag3p4w_6_crc_radio = QRadioButton(self.tag3p4w_6_group)
        self.tag3p4w_6_crc_radio.setObjectName(u"tag3p4w_6_crc_radio")

        self.verticalLayout_117.addWidget(self.tag3p4w_6_crc_radio)

        self.tag3p4w_6_timing_radio = QRadioButton(self.tag3p4w_6_group)
        self.tag3p4w_6_timing_radio.setObjectName(u"tag3p4w_6_timing_radio")

        self.verticalLayout_117.addWidget(self.tag3p4w_6_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_6_group, 1, 1, 1, 1)

        self.tag3p4w_7_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_7_group.setObjectName(u"tag3p4w_7_group")
        self.tag3p4w_7_group.setCheckable(True)
        self.verticalLayout_118 = QVBoxLayout(self.tag3p4w_7_group)
        self.verticalLayout_118.setObjectName(u"verticalLayout_118")
        self.tag3p4w_7_normal_radio = QRadioButton(self.tag3p4w_7_group)
        self.tag3p4w_7_normal_radio.setObjectName(u"tag3p4w_7_normal_radio")
        self.tag3p4w_7_normal_radio.setChecked(True)

        self.verticalLayout_118.addWidget(self.tag3p4w_7_normal_radio)

        self.tag3p4w_7_crc_radio = QRadioButton(self.tag3p4w_7_group)
        self.tag3p4w_7_crc_radio.setObjectName(u"tag3p4w_7_crc_radio")

        self.verticalLayout_118.addWidget(self.tag3p4w_7_crc_radio)

        self.tag3p4w_7_timing_radio = QRadioButton(self.tag3p4w_7_group)
        self.tag3p4w_7_timing_radio.setObjectName(u"tag3p4w_7_timing_radio")

        self.verticalLayout_118.addWidget(self.tag3p4w_7_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_7_group, 1, 2, 1, 1)

        self.tag3p4w_8_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_8_group.setObjectName(u"tag3p4w_8_group")
        self.tag3p4w_8_group.setCheckable(True)
        self.verticalLayout_119 = QVBoxLayout(self.tag3p4w_8_group)
        self.verticalLayout_119.setObjectName(u"verticalLayout_119")
        self.tag3p4w_8_normal_radio = QRadioButton(self.tag3p4w_8_group)
        self.tag3p4w_8_normal_radio.setObjectName(u"tag3p4w_8_normal_radio")
        self.tag3p4w_8_normal_radio.setChecked(True)

        self.verticalLayout_119.addWidget(self.tag3p4w_8_normal_radio)

        self.tag3p4w_8_crc_radio = QRadioButton(self.tag3p4w_8_group)
        self.tag3p4w_8_crc_radio.setObjectName(u"tag3p4w_8_crc_radio")

        self.verticalLayout_119.addWidget(self.tag3p4w_8_crc_radio)

        self.tag3p4w_8_timing_radio = QRadioButton(self.tag3p4w_8_group)
        self.tag3p4w_8_timing_radio.setObjectName(u"tag3p4w_8_timing_radio")

        self.verticalLayout_119.addWidget(self.tag3p4w_8_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_8_group, 1, 3, 1, 1)

        self.tag3p4w_9_group = QGroupBox(self.tag3p4w_tab)
        self.tag3p4w_9_group.setObjectName(u"tag3p4w_9_group")
        self.tag3p4w_9_group.setCheckable(True)
        self.verticalLayout_120 = QVBoxLayout(self.tag3p4w_9_group)
        self.verticalLayout_120.setObjectName(u"verticalLayout_120")
        self.tag3p4w_9_normal_radio = QRadioButton(self.tag3p4w_9_group)
        self.tag3p4w_9_normal_radio.setObjectName(u"tag3p4w_9_normal_radio")
        self.tag3p4w_9_normal_radio.setChecked(True)

        self.verticalLayout_120.addWidget(self.tag3p4w_9_normal_radio)

        self.tag3p4w_9_crc_radio = QRadioButton(self.tag3p4w_9_group)
        self.tag3p4w_9_crc_radio.setObjectName(u"tag3p4w_9_crc_radio")

        self.verticalLayout_120.addWidget(self.tag3p4w_9_crc_radio)

        self.tag3p4w_9_timing_radio = QRadioButton(self.tag3p4w_9_group)
        self.tag3p4w_9_timing_radio.setObjectName(u"tag3p4w_9_timing_radio")

        self.verticalLayout_120.addWidget(self.tag3p4w_9_timing_radio)


        self.gridLayout_18.addWidget(self.tag3p4w_9_group, 1, 4, 1, 1)

        self.device_tab.addTab(self.tag3p4w_tab, "")
        self.oil_tab = QWidget()
        self.oil_tab.setObjectName(u"oil_tab")
        self.gridLayout_5 = QGridLayout(self.oil_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.oil_0_group = QGroupBox(self.oil_tab)
        self.oil_0_group.setObjectName(u"oil_0_group")
        self.oil_0_group.setCheckable(True)
        self.verticalLayout_181 = QVBoxLayout(self.oil_0_group)
        self.verticalLayout_181.setObjectName(u"verticalLayout_181")
        self.oil_0_normal_radio = QRadioButton(self.oil_0_group)
        self.oil_0_normal_radio.setObjectName(u"oil_0_normal_radio")
        self.oil_0_normal_radio.setChecked(True)

        self.verticalLayout_181.addWidget(self.oil_0_normal_radio)

        self.oil_0_crc_radio = QRadioButton(self.oil_0_group)
        self.oil_0_crc_radio.setObjectName(u"oil_0_crc_radio")

        self.verticalLayout_181.addWidget(self.oil_0_crc_radio)

        self.oil_0_timing_radio = QRadioButton(self.oil_0_group)
        self.oil_0_timing_radio.setObjectName(u"oil_0_timing_radio")

        self.verticalLayout_181.addWidget(self.oil_0_timing_radio)


        self.gridLayout_5.addWidget(self.oil_0_group, 0, 0, 1, 1)

        self.oil_1_group = QGroupBox(self.oil_tab)
        self.oil_1_group.setObjectName(u"oil_1_group")
        self.oil_1_group.setCheckable(True)
        self.verticalLayout_189 = QVBoxLayout(self.oil_1_group)
        self.verticalLayout_189.setObjectName(u"verticalLayout_189")
        self.oil_1_normal_radio = QRadioButton(self.oil_1_group)
        self.oil_1_normal_radio.setObjectName(u"oil_1_normal_radio")
        self.oil_1_normal_radio.setChecked(True)

        self.verticalLayout_189.addWidget(self.oil_1_normal_radio)

        self.oil_1_crc_radio = QRadioButton(self.oil_1_group)
        self.oil_1_crc_radio.setObjectName(u"oil_1_crc_radio")

        self.verticalLayout_189.addWidget(self.oil_1_crc_radio)

        self.oil_1_timing_radio = QRadioButton(self.oil_1_group)
        self.oil_1_timing_radio.setObjectName(u"oil_1_timing_radio")

        self.verticalLayout_189.addWidget(self.oil_1_timing_radio)


        self.gridLayout_5.addWidget(self.oil_1_group, 0, 1, 1, 1)

        self.oil_2_group = QGroupBox(self.oil_tab)
        self.oil_2_group.setObjectName(u"oil_2_group")
        self.oil_2_group.setCheckable(True)
        self.verticalLayout_182 = QVBoxLayout(self.oil_2_group)
        self.verticalLayout_182.setObjectName(u"verticalLayout_182")
        self.oil_2_normal_radio = QRadioButton(self.oil_2_group)
        self.oil_2_normal_radio.setObjectName(u"oil_2_normal_radio")
        self.oil_2_normal_radio.setChecked(True)

        self.verticalLayout_182.addWidget(self.oil_2_normal_radio)

        self.oil_2_crc_radio = QRadioButton(self.oil_2_group)
        self.oil_2_crc_radio.setObjectName(u"oil_2_crc_radio")

        self.verticalLayout_182.addWidget(self.oil_2_crc_radio)

        self.oil_2_timing_radio = QRadioButton(self.oil_2_group)
        self.oil_2_timing_radio.setObjectName(u"oil_2_timing_radio")

        self.verticalLayout_182.addWidget(self.oil_2_timing_radio)


        self.gridLayout_5.addWidget(self.oil_2_group, 0, 2, 1, 1)

        self.oil_3_group = QGroupBox(self.oil_tab)
        self.oil_3_group.setObjectName(u"oil_3_group")
        self.oil_3_group.setCheckable(True)
        self.verticalLayout_190 = QVBoxLayout(self.oil_3_group)
        self.verticalLayout_190.setObjectName(u"verticalLayout_190")
        self.oil_3_normal_radio = QRadioButton(self.oil_3_group)
        self.oil_3_normal_radio.setObjectName(u"oil_3_normal_radio")
        self.oil_3_normal_radio.setChecked(True)

        self.verticalLayout_190.addWidget(self.oil_3_normal_radio)

        self.oil_3_crc_radio = QRadioButton(self.oil_3_group)
        self.oil_3_crc_radio.setObjectName(u"oil_3_crc_radio")

        self.verticalLayout_190.addWidget(self.oil_3_crc_radio)

        self.oil_3_timing_radio = QRadioButton(self.oil_3_group)
        self.oil_3_timing_radio.setObjectName(u"oil_3_timing_radio")

        self.verticalLayout_190.addWidget(self.oil_3_timing_radio)


        self.gridLayout_5.addWidget(self.oil_3_group, 0, 3, 1, 1)

        self.oil_4_group = QGroupBox(self.oil_tab)
        self.oil_4_group.setObjectName(u"oil_4_group")
        self.oil_4_group.setCheckable(True)
        self.verticalLayout_185 = QVBoxLayout(self.oil_4_group)
        self.verticalLayout_185.setObjectName(u"verticalLayout_185")
        self.oil_4_normal_radio = QRadioButton(self.oil_4_group)
        self.oil_4_normal_radio.setObjectName(u"oil_4_normal_radio")
        self.oil_4_normal_radio.setChecked(True)

        self.verticalLayout_185.addWidget(self.oil_4_normal_radio)

        self.oil_4_crc_radio = QRadioButton(self.oil_4_group)
        self.oil_4_crc_radio.setObjectName(u"oil_4_crc_radio")

        self.verticalLayout_185.addWidget(self.oil_4_crc_radio)

        self.oil_4_timing_radio = QRadioButton(self.oil_4_group)
        self.oil_4_timing_radio.setObjectName(u"oil_4_timing_radio")

        self.verticalLayout_185.addWidget(self.oil_4_timing_radio)


        self.gridLayout_5.addWidget(self.oil_4_group, 0, 4, 1, 1)

        self.oil_5_group = QGroupBox(self.oil_tab)
        self.oil_5_group.setObjectName(u"oil_5_group")
        self.oil_5_group.setCheckable(True)
        self.verticalLayout_183 = QVBoxLayout(self.oil_5_group)
        self.verticalLayout_183.setObjectName(u"verticalLayout_183")
        self.oil_5_normal_radio = QRadioButton(self.oil_5_group)
        self.oil_5_normal_radio.setObjectName(u"oil_5_normal_radio")
        self.oil_5_normal_radio.setChecked(True)

        self.verticalLayout_183.addWidget(self.oil_5_normal_radio)

        self.oil_5_crc_radio = QRadioButton(self.oil_5_group)
        self.oil_5_crc_radio.setObjectName(u"oil_5_crc_radio")

        self.verticalLayout_183.addWidget(self.oil_5_crc_radio)

        self.oil_5_timing_radio = QRadioButton(self.oil_5_group)
        self.oil_5_timing_radio.setObjectName(u"oil_5_timing_radio")

        self.verticalLayout_183.addWidget(self.oil_5_timing_radio)


        self.gridLayout_5.addWidget(self.oil_5_group, 1, 0, 1, 1)

        self.oil_6_group = QGroupBox(self.oil_tab)
        self.oil_6_group.setObjectName(u"oil_6_group")
        self.oil_6_group.setCheckable(True)
        self.verticalLayout_188 = QVBoxLayout(self.oil_6_group)
        self.verticalLayout_188.setObjectName(u"verticalLayout_188")
        self.oil_6_normal_radio = QRadioButton(self.oil_6_group)
        self.oil_6_normal_radio.setObjectName(u"oil_6_normal_radio")
        self.oil_6_normal_radio.setChecked(True)

        self.verticalLayout_188.addWidget(self.oil_6_normal_radio)

        self.oil_6_crc_radio = QRadioButton(self.oil_6_group)
        self.oil_6_crc_radio.setObjectName(u"oil_6_crc_radio")

        self.verticalLayout_188.addWidget(self.oil_6_crc_radio)

        self.oil_6_timing_radio = QRadioButton(self.oil_6_group)
        self.oil_6_timing_radio.setObjectName(u"oil_6_timing_radio")

        self.verticalLayout_188.addWidget(self.oil_6_timing_radio)


        self.gridLayout_5.addWidget(self.oil_6_group, 1, 1, 1, 1)

        self.oil_7_group = QGroupBox(self.oil_tab)
        self.oil_7_group.setObjectName(u"oil_7_group")
        self.oil_7_group.setCheckable(True)
        self.verticalLayout_187 = QVBoxLayout(self.oil_7_group)
        self.verticalLayout_187.setObjectName(u"verticalLayout_187")
        self.oil_7_normal_radio = QRadioButton(self.oil_7_group)
        self.oil_7_normal_radio.setObjectName(u"oil_7_normal_radio")
        self.oil_7_normal_radio.setChecked(True)

        self.verticalLayout_187.addWidget(self.oil_7_normal_radio)

        self.oil_7_crc_radio = QRadioButton(self.oil_7_group)
        self.oil_7_crc_radio.setObjectName(u"oil_7_crc_radio")

        self.verticalLayout_187.addWidget(self.oil_7_crc_radio)

        self.oil_7_timing_radio = QRadioButton(self.oil_7_group)
        self.oil_7_timing_radio.setObjectName(u"oil_7_timing_radio")

        self.verticalLayout_187.addWidget(self.oil_7_timing_radio)


        self.gridLayout_5.addWidget(self.oil_7_group, 1, 2, 1, 1)

        self.oil_8_group = QGroupBox(self.oil_tab)
        self.oil_8_group.setObjectName(u"oil_8_group")
        self.oil_8_group.setCheckable(True)
        self.verticalLayout_184 = QVBoxLayout(self.oil_8_group)
        self.verticalLayout_184.setObjectName(u"verticalLayout_184")
        self.oil_8_normal_radio = QRadioButton(self.oil_8_group)
        self.oil_8_normal_radio.setObjectName(u"oil_8_normal_radio")
        self.oil_8_normal_radio.setChecked(True)

        self.verticalLayout_184.addWidget(self.oil_8_normal_radio)

        self.oil_8_crc_radio = QRadioButton(self.oil_8_group)
        self.oil_8_crc_radio.setObjectName(u"oil_8_crc_radio")

        self.verticalLayout_184.addWidget(self.oil_8_crc_radio)

        self.oil_8_timing_radio = QRadioButton(self.oil_8_group)
        self.oil_8_timing_radio.setObjectName(u"oil_8_timing_radio")

        self.verticalLayout_184.addWidget(self.oil_8_timing_radio)


        self.gridLayout_5.addWidget(self.oil_8_group, 1, 3, 1, 1)

        self.oil_9_group = QGroupBox(self.oil_tab)
        self.oil_9_group.setObjectName(u"oil_9_group")
        self.oil_9_group.setCheckable(True)
        self.verticalLayout_186 = QVBoxLayout(self.oil_9_group)
        self.verticalLayout_186.setObjectName(u"verticalLayout_186")
        self.oil_9_normal_radio = QRadioButton(self.oil_9_group)
        self.oil_9_normal_radio.setObjectName(u"oil_9_normal_radio")
        self.oil_9_normal_radio.setChecked(True)

        self.verticalLayout_186.addWidget(self.oil_9_normal_radio)

        self.oil_9_crc_radio = QRadioButton(self.oil_9_group)
        self.oil_9_crc_radio.setObjectName(u"oil_9_crc_radio")

        self.verticalLayout_186.addWidget(self.oil_9_crc_radio)

        self.oil_9_timing_radio = QRadioButton(self.oil_9_group)
        self.oil_9_timing_radio.setObjectName(u"oil_9_timing_radio")

        self.verticalLayout_186.addWidget(self.oil_9_timing_radio)


        self.gridLayout_5.addWidget(self.oil_9_group, 1, 4, 1, 1)

        self.device_tab.addTab(self.oil_tab, "")
        self.water_tab = QWidget()
        self.water_tab.setObjectName(u"water_tab")
        self.gridLayout_4 = QGridLayout(self.water_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.water_0_group = QGroupBox(self.water_tab)
        self.water_0_group.setObjectName(u"water_0_group")
        self.water_0_group.setCheckable(True)
        self.verticalLayout_121 = QVBoxLayout(self.water_0_group)
        self.verticalLayout_121.setObjectName(u"verticalLayout_121")
        self.water_0_normal_radio = QRadioButton(self.water_0_group)
        self.water_0_normal_radio.setObjectName(u"water_0_normal_radio")
        self.water_0_normal_radio.setChecked(True)

        self.verticalLayout_121.addWidget(self.water_0_normal_radio)

        self.water_0_crc_radio = QRadioButton(self.water_0_group)
        self.water_0_crc_radio.setObjectName(u"water_0_crc_radio")

        self.verticalLayout_121.addWidget(self.water_0_crc_radio)

        self.water_0_timing_radio = QRadioButton(self.water_0_group)
        self.water_0_timing_radio.setObjectName(u"water_0_timing_radio")

        self.verticalLayout_121.addWidget(self.water_0_timing_radio)


        self.gridLayout_4.addWidget(self.water_0_group, 0, 0, 1, 1)

        self.water_1_group = QGroupBox(self.water_tab)
        self.water_1_group.setObjectName(u"water_1_group")
        self.water_1_group.setCheckable(True)
        self.verticalLayout_122 = QVBoxLayout(self.water_1_group)
        self.verticalLayout_122.setObjectName(u"verticalLayout_122")
        self.water_1_normal_radio = QRadioButton(self.water_1_group)
        self.water_1_normal_radio.setObjectName(u"water_1_normal_radio")
        self.water_1_normal_radio.setChecked(True)

        self.verticalLayout_122.addWidget(self.water_1_normal_radio)

        self.water_1_crc_radio = QRadioButton(self.water_1_group)
        self.water_1_crc_radio.setObjectName(u"water_1_crc_radio")

        self.verticalLayout_122.addWidget(self.water_1_crc_radio)

        self.water_1_timing_radio = QRadioButton(self.water_1_group)
        self.water_1_timing_radio.setObjectName(u"water_1_timing_radio")

        self.verticalLayout_122.addWidget(self.water_1_timing_radio)


        self.gridLayout_4.addWidget(self.water_1_group, 0, 1, 1, 1)

        self.water_2_group = QGroupBox(self.water_tab)
        self.water_2_group.setObjectName(u"water_2_group")
        self.water_2_group.setCheckable(True)
        self.verticalLayout_123 = QVBoxLayout(self.water_2_group)
        self.verticalLayout_123.setObjectName(u"verticalLayout_123")
        self.water_2_normal_radio = QRadioButton(self.water_2_group)
        self.water_2_normal_radio.setObjectName(u"water_2_normal_radio")
        self.water_2_normal_radio.setChecked(True)

        self.verticalLayout_123.addWidget(self.water_2_normal_radio)

        self.water_2_crc_radio = QRadioButton(self.water_2_group)
        self.water_2_crc_radio.setObjectName(u"water_2_crc_radio")

        self.verticalLayout_123.addWidget(self.water_2_crc_radio)

        self.water_2_timing_radio = QRadioButton(self.water_2_group)
        self.water_2_timing_radio.setObjectName(u"water_2_timing_radio")

        self.verticalLayout_123.addWidget(self.water_2_timing_radio)


        self.gridLayout_4.addWidget(self.water_2_group, 0, 2, 1, 1)

        self.water_3_group = QGroupBox(self.water_tab)
        self.water_3_group.setObjectName(u"water_3_group")
        self.water_3_group.setCheckable(True)
        self.verticalLayout_124 = QVBoxLayout(self.water_3_group)
        self.verticalLayout_124.setObjectName(u"verticalLayout_124")
        self.water_3_normal_radio = QRadioButton(self.water_3_group)
        self.water_3_normal_radio.setObjectName(u"water_3_normal_radio")
        self.water_3_normal_radio.setChecked(True)

        self.verticalLayout_124.addWidget(self.water_3_normal_radio)

        self.water_3_crc_radio = QRadioButton(self.water_3_group)
        self.water_3_crc_radio.setObjectName(u"water_3_crc_radio")

        self.verticalLayout_124.addWidget(self.water_3_crc_radio)

        self.water_3_timing_radio = QRadioButton(self.water_3_group)
        self.water_3_timing_radio.setObjectName(u"water_3_timing_radio")

        self.verticalLayout_124.addWidget(self.water_3_timing_radio)


        self.gridLayout_4.addWidget(self.water_3_group, 0, 3, 1, 1)

        self.water_4_group = QGroupBox(self.water_tab)
        self.water_4_group.setObjectName(u"water_4_group")
        self.water_4_group.setCheckable(True)
        self.verticalLayout_125 = QVBoxLayout(self.water_4_group)
        self.verticalLayout_125.setObjectName(u"verticalLayout_125")
        self.water_4_normal_radio = QRadioButton(self.water_4_group)
        self.water_4_normal_radio.setObjectName(u"water_4_normal_radio")
        self.water_4_normal_radio.setChecked(True)

        self.verticalLayout_125.addWidget(self.water_4_normal_radio)

        self.water_4_crc_radio = QRadioButton(self.water_4_group)
        self.water_4_crc_radio.setObjectName(u"water_4_crc_radio")

        self.verticalLayout_125.addWidget(self.water_4_crc_radio)

        self.water_4_timing_radio = QRadioButton(self.water_4_group)
        self.water_4_timing_radio.setObjectName(u"water_4_timing_radio")

        self.verticalLayout_125.addWidget(self.water_4_timing_radio)


        self.gridLayout_4.addWidget(self.water_4_group, 0, 4, 1, 1)

        self.water_5_group = QGroupBox(self.water_tab)
        self.water_5_group.setObjectName(u"water_5_group")
        self.water_5_group.setCheckable(True)
        self.verticalLayout_126 = QVBoxLayout(self.water_5_group)
        self.verticalLayout_126.setObjectName(u"verticalLayout_126")
        self.water_5_normal_radio = QRadioButton(self.water_5_group)
        self.water_5_normal_radio.setObjectName(u"water_5_normal_radio")
        self.water_5_normal_radio.setChecked(True)

        self.verticalLayout_126.addWidget(self.water_5_normal_radio)

        self.water_5_crc_radio = QRadioButton(self.water_5_group)
        self.water_5_crc_radio.setObjectName(u"water_5_crc_radio")

        self.verticalLayout_126.addWidget(self.water_5_crc_radio)

        self.water_5_timing_radio = QRadioButton(self.water_5_group)
        self.water_5_timing_radio.setObjectName(u"water_5_timing_radio")

        self.verticalLayout_126.addWidget(self.water_5_timing_radio)


        self.gridLayout_4.addWidget(self.water_5_group, 1, 0, 1, 1)

        self.water_6_group = QGroupBox(self.water_tab)
        self.water_6_group.setObjectName(u"water_6_group")
        self.water_6_group.setCheckable(True)
        self.verticalLayout_127 = QVBoxLayout(self.water_6_group)
        self.verticalLayout_127.setObjectName(u"verticalLayout_127")
        self.water_6_normal_radio = QRadioButton(self.water_6_group)
        self.water_6_normal_radio.setObjectName(u"water_6_normal_radio")
        self.water_6_normal_radio.setChecked(True)

        self.verticalLayout_127.addWidget(self.water_6_normal_radio)

        self.water_6_crc_radio = QRadioButton(self.water_6_group)
        self.water_6_crc_radio.setObjectName(u"water_6_crc_radio")

        self.verticalLayout_127.addWidget(self.water_6_crc_radio)

        self.water_6_timing_radio = QRadioButton(self.water_6_group)
        self.water_6_timing_radio.setObjectName(u"water_6_timing_radio")

        self.verticalLayout_127.addWidget(self.water_6_timing_radio)


        self.gridLayout_4.addWidget(self.water_6_group, 1, 1, 1, 1)

        self.water_7_group = QGroupBox(self.water_tab)
        self.water_7_group.setObjectName(u"water_7_group")
        self.water_7_group.setCheckable(True)
        self.verticalLayout_128 = QVBoxLayout(self.water_7_group)
        self.verticalLayout_128.setObjectName(u"verticalLayout_128")
        self.water_7_normal_radio = QRadioButton(self.water_7_group)
        self.water_7_normal_radio.setObjectName(u"water_7_normal_radio")
        self.water_7_normal_radio.setChecked(True)

        self.verticalLayout_128.addWidget(self.water_7_normal_radio)

        self.water_7_crc_radio = QRadioButton(self.water_7_group)
        self.water_7_crc_radio.setObjectName(u"water_7_crc_radio")

        self.verticalLayout_128.addWidget(self.water_7_crc_radio)

        self.water_7_timing_radio = QRadioButton(self.water_7_group)
        self.water_7_timing_radio.setObjectName(u"water_7_timing_radio")

        self.verticalLayout_128.addWidget(self.water_7_timing_radio)


        self.gridLayout_4.addWidget(self.water_7_group, 1, 2, 1, 1)

        self.water_8_group = QGroupBox(self.water_tab)
        self.water_8_group.setObjectName(u"water_8_group")
        self.water_8_group.setCheckable(True)
        self.verticalLayout_129 = QVBoxLayout(self.water_8_group)
        self.verticalLayout_129.setObjectName(u"verticalLayout_129")
        self.water_8_normal_radio = QRadioButton(self.water_8_group)
        self.water_8_normal_radio.setObjectName(u"water_8_normal_radio")
        self.water_8_normal_radio.setChecked(True)

        self.verticalLayout_129.addWidget(self.water_8_normal_radio)

        self.water_8_crc_radio = QRadioButton(self.water_8_group)
        self.water_8_crc_radio.setObjectName(u"water_8_crc_radio")

        self.verticalLayout_129.addWidget(self.water_8_crc_radio)

        self.water_8_timing_radio = QRadioButton(self.water_8_group)
        self.water_8_timing_radio.setObjectName(u"water_8_timing_radio")

        self.verticalLayout_129.addWidget(self.water_8_timing_radio)


        self.gridLayout_4.addWidget(self.water_8_group, 1, 3, 1, 1)

        self.water_9_group = QGroupBox(self.water_tab)
        self.water_9_group.setObjectName(u"water_9_group")
        self.water_9_group.setCheckable(True)
        self.verticalLayout_130 = QVBoxLayout(self.water_9_group)
        self.verticalLayout_130.setObjectName(u"verticalLayout_130")
        self.water_9_normal_radio = QRadioButton(self.water_9_group)
        self.water_9_normal_radio.setObjectName(u"water_9_normal_radio")
        self.water_9_normal_radio.setChecked(True)

        self.verticalLayout_130.addWidget(self.water_9_normal_radio)

        self.water_9_crc_radio = QRadioButton(self.water_9_group)
        self.water_9_crc_radio.setObjectName(u"water_9_crc_radio")

        self.verticalLayout_130.addWidget(self.water_9_crc_radio)

        self.water_9_timing_radio = QRadioButton(self.water_9_group)
        self.water_9_timing_radio.setObjectName(u"water_9_timing_radio")

        self.verticalLayout_130.addWidget(self.water_9_timing_radio)


        self.gridLayout_4.addWidget(self.water_9_group, 1, 4, 1, 1)

        self.device_tab.addTab(self.water_tab, "")
        self.co2_tab = QWidget()
        self.co2_tab.setObjectName(u"co2_tab")
        self.gridLayout_21 = QGridLayout(self.co2_tab)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.co2_0_group = QGroupBox(self.co2_tab)
        self.co2_0_group.setObjectName(u"co2_0_group")
        self.co2_0_group.setCheckable(True)
        self.verticalLayout_141 = QVBoxLayout(self.co2_0_group)
        self.verticalLayout_141.setObjectName(u"verticalLayout_141")
        self.co2_0_normal_radio = QRadioButton(self.co2_0_group)
        self.co2_0_normal_radio.setObjectName(u"co2_0_normal_radio")
        self.co2_0_normal_radio.setChecked(True)

        self.verticalLayout_141.addWidget(self.co2_0_normal_radio)

        self.co2_0_crc_radio = QRadioButton(self.co2_0_group)
        self.co2_0_crc_radio.setObjectName(u"co2_0_crc_radio")

        self.verticalLayout_141.addWidget(self.co2_0_crc_radio)

        self.co2_0_timing_radio = QRadioButton(self.co2_0_group)
        self.co2_0_timing_radio.setObjectName(u"co2_0_timing_radio")

        self.verticalLayout_141.addWidget(self.co2_0_timing_radio)


        self.gridLayout_21.addWidget(self.co2_0_group, 0, 0, 1, 1)

        self.co2_1_group = QGroupBox(self.co2_tab)
        self.co2_1_group.setObjectName(u"co2_1_group")
        self.co2_1_group.setCheckable(True)
        self.verticalLayout_142 = QVBoxLayout(self.co2_1_group)
        self.verticalLayout_142.setObjectName(u"verticalLayout_142")
        self.co2_1_normal_radio = QRadioButton(self.co2_1_group)
        self.co2_1_normal_radio.setObjectName(u"co2_1_normal_radio")
        self.co2_1_normal_radio.setChecked(True)

        self.verticalLayout_142.addWidget(self.co2_1_normal_radio)

        self.co2_1_crc_radio = QRadioButton(self.co2_1_group)
        self.co2_1_crc_radio.setObjectName(u"co2_1_crc_radio")

        self.verticalLayout_142.addWidget(self.co2_1_crc_radio)

        self.co2_1_timing_radio = QRadioButton(self.co2_1_group)
        self.co2_1_timing_radio.setObjectName(u"co2_1_timing_radio")

        self.verticalLayout_142.addWidget(self.co2_1_timing_radio)


        self.gridLayout_21.addWidget(self.co2_1_group, 0, 1, 1, 1)

        self.co2_2_group = QGroupBox(self.co2_tab)
        self.co2_2_group.setObjectName(u"co2_2_group")
        self.co2_2_group.setCheckable(True)
        self.verticalLayout_143 = QVBoxLayout(self.co2_2_group)
        self.verticalLayout_143.setObjectName(u"verticalLayout_143")
        self.co2_2_normal_radio = QRadioButton(self.co2_2_group)
        self.co2_2_normal_radio.setObjectName(u"co2_2_normal_radio")
        self.co2_2_normal_radio.setChecked(True)

        self.verticalLayout_143.addWidget(self.co2_2_normal_radio)

        self.co2_2_crc_radio = QRadioButton(self.co2_2_group)
        self.co2_2_crc_radio.setObjectName(u"co2_2_crc_radio")

        self.verticalLayout_143.addWidget(self.co2_2_crc_radio)

        self.co2_2_timing_radio = QRadioButton(self.co2_2_group)
        self.co2_2_timing_radio.setObjectName(u"co2_2_timing_radio")

        self.verticalLayout_143.addWidget(self.co2_2_timing_radio)


        self.gridLayout_21.addWidget(self.co2_2_group, 0, 2, 1, 1)

        self.co2_3_group = QGroupBox(self.co2_tab)
        self.co2_3_group.setObjectName(u"co2_3_group")
        self.co2_3_group.setCheckable(True)
        self.verticalLayout_144 = QVBoxLayout(self.co2_3_group)
        self.verticalLayout_144.setObjectName(u"verticalLayout_144")
        self.co2_3_normal_radio = QRadioButton(self.co2_3_group)
        self.co2_3_normal_radio.setObjectName(u"co2_3_normal_radio")
        self.co2_3_normal_radio.setChecked(True)

        self.verticalLayout_144.addWidget(self.co2_3_normal_radio)

        self.co2_3_crc_radio = QRadioButton(self.co2_3_group)
        self.co2_3_crc_radio.setObjectName(u"co2_3_crc_radio")

        self.verticalLayout_144.addWidget(self.co2_3_crc_radio)

        self.co2_3_timing_radio = QRadioButton(self.co2_3_group)
        self.co2_3_timing_radio.setObjectName(u"co2_3_timing_radio")

        self.verticalLayout_144.addWidget(self.co2_3_timing_radio)


        self.gridLayout_21.addWidget(self.co2_3_group, 0, 3, 1, 1)

        self.co2_4_group = QGroupBox(self.co2_tab)
        self.co2_4_group.setObjectName(u"co2_4_group")
        self.co2_4_group.setCheckable(True)
        self.verticalLayout_145 = QVBoxLayout(self.co2_4_group)
        self.verticalLayout_145.setObjectName(u"verticalLayout_145")
        self.co2_4_normal_radio = QRadioButton(self.co2_4_group)
        self.co2_4_normal_radio.setObjectName(u"co2_4_normal_radio")
        self.co2_4_normal_radio.setChecked(True)

        self.verticalLayout_145.addWidget(self.co2_4_normal_radio)

        self.co2_4_crc_radio = QRadioButton(self.co2_4_group)
        self.co2_4_crc_radio.setObjectName(u"co2_4_crc_radio")

        self.verticalLayout_145.addWidget(self.co2_4_crc_radio)

        self.co2_4_timing_radio = QRadioButton(self.co2_4_group)
        self.co2_4_timing_radio.setObjectName(u"co2_4_timing_radio")

        self.verticalLayout_145.addWidget(self.co2_4_timing_radio)


        self.gridLayout_21.addWidget(self.co2_4_group, 0, 4, 1, 1)

        self.co2_5_group = QGroupBox(self.co2_tab)
        self.co2_5_group.setObjectName(u"co2_5_group")
        self.co2_5_group.setCheckable(True)
        self.verticalLayout_146 = QVBoxLayout(self.co2_5_group)
        self.verticalLayout_146.setObjectName(u"verticalLayout_146")
        self.co2_5_normal_radio = QRadioButton(self.co2_5_group)
        self.co2_5_normal_radio.setObjectName(u"co2_5_normal_radio")
        self.co2_5_normal_radio.setChecked(True)

        self.verticalLayout_146.addWidget(self.co2_5_normal_radio)

        self.co2_5_crc_radio = QRadioButton(self.co2_5_group)
        self.co2_5_crc_radio.setObjectName(u"co2_5_crc_radio")

        self.verticalLayout_146.addWidget(self.co2_5_crc_radio)

        self.co2_5_timing_radio = QRadioButton(self.co2_5_group)
        self.co2_5_timing_radio.setObjectName(u"co2_5_timing_radio")

        self.verticalLayout_146.addWidget(self.co2_5_timing_radio)


        self.gridLayout_21.addWidget(self.co2_5_group, 1, 0, 1, 1)

        self.co2_6_group = QGroupBox(self.co2_tab)
        self.co2_6_group.setObjectName(u"co2_6_group")
        self.co2_6_group.setCheckable(True)
        self.verticalLayout_147 = QVBoxLayout(self.co2_6_group)
        self.verticalLayout_147.setObjectName(u"verticalLayout_147")
        self.co2_6_normal_radio = QRadioButton(self.co2_6_group)
        self.co2_6_normal_radio.setObjectName(u"co2_6_normal_radio")
        self.co2_6_normal_radio.setChecked(True)

        self.verticalLayout_147.addWidget(self.co2_6_normal_radio)

        self.co2_6_crc_radio = QRadioButton(self.co2_6_group)
        self.co2_6_crc_radio.setObjectName(u"co2_6_crc_radio")

        self.verticalLayout_147.addWidget(self.co2_6_crc_radio)

        self.co2_6_timing_radio = QRadioButton(self.co2_6_group)
        self.co2_6_timing_radio.setObjectName(u"co2_6_timing_radio")

        self.verticalLayout_147.addWidget(self.co2_6_timing_radio)


        self.gridLayout_21.addWidget(self.co2_6_group, 1, 1, 1, 1)

        self.co2_7_group = QGroupBox(self.co2_tab)
        self.co2_7_group.setObjectName(u"co2_7_group")
        self.co2_7_group.setCheckable(True)
        self.verticalLayout_148 = QVBoxLayout(self.co2_7_group)
        self.verticalLayout_148.setObjectName(u"verticalLayout_148")
        self.co2_7_normal_radio = QRadioButton(self.co2_7_group)
        self.co2_7_normal_radio.setObjectName(u"co2_7_normal_radio")
        self.co2_7_normal_radio.setChecked(True)

        self.verticalLayout_148.addWidget(self.co2_7_normal_radio)

        self.co2_7_crc_radio = QRadioButton(self.co2_7_group)
        self.co2_7_crc_radio.setObjectName(u"co2_7_crc_radio")

        self.verticalLayout_148.addWidget(self.co2_7_crc_radio)

        self.co2_7_timing_radio = QRadioButton(self.co2_7_group)
        self.co2_7_timing_radio.setObjectName(u"co2_7_timing_radio")

        self.verticalLayout_148.addWidget(self.co2_7_timing_radio)


        self.gridLayout_21.addWidget(self.co2_7_group, 1, 2, 1, 1)

        self.co2_8_group = QGroupBox(self.co2_tab)
        self.co2_8_group.setObjectName(u"co2_8_group")
        self.co2_8_group.setCheckable(True)
        self.verticalLayout_149 = QVBoxLayout(self.co2_8_group)
        self.verticalLayout_149.setObjectName(u"verticalLayout_149")
        self.co2_8_normal_radio = QRadioButton(self.co2_8_group)
        self.co2_8_normal_radio.setObjectName(u"co2_8_normal_radio")
        self.co2_8_normal_radio.setChecked(True)

        self.verticalLayout_149.addWidget(self.co2_8_normal_radio)

        self.co2_8_crc_radio = QRadioButton(self.co2_8_group)
        self.co2_8_crc_radio.setObjectName(u"co2_8_crc_radio")

        self.verticalLayout_149.addWidget(self.co2_8_crc_radio)

        self.co2_8_timing_radio = QRadioButton(self.co2_8_group)
        self.co2_8_timing_radio.setObjectName(u"co2_8_timing_radio")

        self.verticalLayout_149.addWidget(self.co2_8_timing_radio)


        self.gridLayout_21.addWidget(self.co2_8_group, 1, 3, 1, 1)

        self.co2_9_group = QGroupBox(self.co2_tab)
        self.co2_9_group.setObjectName(u"co2_9_group")
        self.co2_9_group.setCheckable(True)
        self.verticalLayout_150 = QVBoxLayout(self.co2_9_group)
        self.verticalLayout_150.setObjectName(u"verticalLayout_150")
        self.co2_9_normal_radio = QRadioButton(self.co2_9_group)
        self.co2_9_normal_radio.setObjectName(u"co2_9_normal_radio")
        self.co2_9_normal_radio.setChecked(True)

        self.verticalLayout_150.addWidget(self.co2_9_normal_radio)

        self.co2_9_crc_radio = QRadioButton(self.co2_9_group)
        self.co2_9_crc_radio.setObjectName(u"co2_9_crc_radio")

        self.verticalLayout_150.addWidget(self.co2_9_crc_radio)

        self.co2_9_timing_radio = QRadioButton(self.co2_9_group)
        self.co2_9_timing_radio.setObjectName(u"co2_9_timing_radio")

        self.verticalLayout_150.addWidget(self.co2_9_timing_radio)


        self.gridLayout_21.addWidget(self.co2_9_group, 1, 4, 1, 1)

        self.device_tab.addTab(self.co2_tab, "")
        self.temperature_tab = QWidget()
        self.temperature_tab.setObjectName(u"temperature_tab")
        self.gridLayout_6 = QGridLayout(self.temperature_tab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.co2_0_group_2 = QGroupBox(self.temperature_tab)
        self.co2_0_group_2.setObjectName(u"co2_0_group_2")
        self.co2_0_group_2.setCheckable(True)
        self.verticalLayout_151 = QVBoxLayout(self.co2_0_group_2)
        self.verticalLayout_151.setObjectName(u"verticalLayout_151")
        self.co2_0_normal_radio_2 = QRadioButton(self.co2_0_group_2)
        self.co2_0_normal_radio_2.setObjectName(u"co2_0_normal_radio_2")
        self.co2_0_normal_radio_2.setChecked(True)

        self.verticalLayout_151.addWidget(self.co2_0_normal_radio_2)

        self.co2_0_crc_radio_2 = QRadioButton(self.co2_0_group_2)
        self.co2_0_crc_radio_2.setObjectName(u"co2_0_crc_radio_2")

        self.verticalLayout_151.addWidget(self.co2_0_crc_radio_2)

        self.co2_0_timing_radio_2 = QRadioButton(self.co2_0_group_2)
        self.co2_0_timing_radio_2.setObjectName(u"co2_0_timing_radio_2")

        self.verticalLayout_151.addWidget(self.co2_0_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_0_group_2, 0, 0, 1, 1)

        self.co2_1_group_2 = QGroupBox(self.temperature_tab)
        self.co2_1_group_2.setObjectName(u"co2_1_group_2")
        self.co2_1_group_2.setCheckable(True)
        self.verticalLayout_159 = QVBoxLayout(self.co2_1_group_2)
        self.verticalLayout_159.setObjectName(u"verticalLayout_159")
        self.co2_1_normal_radio_2 = QRadioButton(self.co2_1_group_2)
        self.co2_1_normal_radio_2.setObjectName(u"co2_1_normal_radio_2")
        self.co2_1_normal_radio_2.setChecked(True)

        self.verticalLayout_159.addWidget(self.co2_1_normal_radio_2)

        self.co2_1_crc_radio_2 = QRadioButton(self.co2_1_group_2)
        self.co2_1_crc_radio_2.setObjectName(u"co2_1_crc_radio_2")

        self.verticalLayout_159.addWidget(self.co2_1_crc_radio_2)

        self.co2_1_timing_radio_2 = QRadioButton(self.co2_1_group_2)
        self.co2_1_timing_radio_2.setObjectName(u"co2_1_timing_radio_2")

        self.verticalLayout_159.addWidget(self.co2_1_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_1_group_2, 0, 1, 1, 1)

        self.co2_2_group_2 = QGroupBox(self.temperature_tab)
        self.co2_2_group_2.setObjectName(u"co2_2_group_2")
        self.co2_2_group_2.setCheckable(True)
        self.verticalLayout_152 = QVBoxLayout(self.co2_2_group_2)
        self.verticalLayout_152.setObjectName(u"verticalLayout_152")
        self.co2_2_normal_radio_2 = QRadioButton(self.co2_2_group_2)
        self.co2_2_normal_radio_2.setObjectName(u"co2_2_normal_radio_2")
        self.co2_2_normal_radio_2.setChecked(True)

        self.verticalLayout_152.addWidget(self.co2_2_normal_radio_2)

        self.co2_2_crc_radio_2 = QRadioButton(self.co2_2_group_2)
        self.co2_2_crc_radio_2.setObjectName(u"co2_2_crc_radio_2")

        self.verticalLayout_152.addWidget(self.co2_2_crc_radio_2)

        self.co2_2_timing_radio_2 = QRadioButton(self.co2_2_group_2)
        self.co2_2_timing_radio_2.setObjectName(u"co2_2_timing_radio_2")

        self.verticalLayout_152.addWidget(self.co2_2_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_2_group_2, 0, 2, 1, 1)

        self.co2_3_group_2 = QGroupBox(self.temperature_tab)
        self.co2_3_group_2.setObjectName(u"co2_3_group_2")
        self.co2_3_group_2.setCheckable(True)
        self.verticalLayout_160 = QVBoxLayout(self.co2_3_group_2)
        self.verticalLayout_160.setObjectName(u"verticalLayout_160")
        self.co2_3_normal_radio_2 = QRadioButton(self.co2_3_group_2)
        self.co2_3_normal_radio_2.setObjectName(u"co2_3_normal_radio_2")
        self.co2_3_normal_radio_2.setChecked(True)

        self.verticalLayout_160.addWidget(self.co2_3_normal_radio_2)

        self.co2_3_crc_radio_2 = QRadioButton(self.co2_3_group_2)
        self.co2_3_crc_radio_2.setObjectName(u"co2_3_crc_radio_2")

        self.verticalLayout_160.addWidget(self.co2_3_crc_radio_2)

        self.co2_3_timing_radio_2 = QRadioButton(self.co2_3_group_2)
        self.co2_3_timing_radio_2.setObjectName(u"co2_3_timing_radio_2")

        self.verticalLayout_160.addWidget(self.co2_3_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_3_group_2, 0, 3, 1, 1)

        self.co2_4_group_2 = QGroupBox(self.temperature_tab)
        self.co2_4_group_2.setObjectName(u"co2_4_group_2")
        self.co2_4_group_2.setCheckable(True)
        self.verticalLayout_155 = QVBoxLayout(self.co2_4_group_2)
        self.verticalLayout_155.setObjectName(u"verticalLayout_155")
        self.co2_4_normal_radio_2 = QRadioButton(self.co2_4_group_2)
        self.co2_4_normal_radio_2.setObjectName(u"co2_4_normal_radio_2")
        self.co2_4_normal_radio_2.setChecked(True)

        self.verticalLayout_155.addWidget(self.co2_4_normal_radio_2)

        self.co2_4_crc_radio_2 = QRadioButton(self.co2_4_group_2)
        self.co2_4_crc_radio_2.setObjectName(u"co2_4_crc_radio_2")

        self.verticalLayout_155.addWidget(self.co2_4_crc_radio_2)

        self.co2_4_timing_radio_2 = QRadioButton(self.co2_4_group_2)
        self.co2_4_timing_radio_2.setObjectName(u"co2_4_timing_radio_2")

        self.verticalLayout_155.addWidget(self.co2_4_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_4_group_2, 0, 4, 1, 1)

        self.co2_5_group_2 = QGroupBox(self.temperature_tab)
        self.co2_5_group_2.setObjectName(u"co2_5_group_2")
        self.co2_5_group_2.setCheckable(True)
        self.verticalLayout_153 = QVBoxLayout(self.co2_5_group_2)
        self.verticalLayout_153.setObjectName(u"verticalLayout_153")
        self.co2_5_normal_radio_2 = QRadioButton(self.co2_5_group_2)
        self.co2_5_normal_radio_2.setObjectName(u"co2_5_normal_radio_2")
        self.co2_5_normal_radio_2.setChecked(True)

        self.verticalLayout_153.addWidget(self.co2_5_normal_radio_2)

        self.co2_5_crc_radio_2 = QRadioButton(self.co2_5_group_2)
        self.co2_5_crc_radio_2.setObjectName(u"co2_5_crc_radio_2")

        self.verticalLayout_153.addWidget(self.co2_5_crc_radio_2)

        self.co2_5_timing_radio_2 = QRadioButton(self.co2_5_group_2)
        self.co2_5_timing_radio_2.setObjectName(u"co2_5_timing_radio_2")

        self.verticalLayout_153.addWidget(self.co2_5_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_5_group_2, 1, 0, 1, 1)

        self.co2_6_group_2 = QGroupBox(self.temperature_tab)
        self.co2_6_group_2.setObjectName(u"co2_6_group_2")
        self.co2_6_group_2.setCheckable(True)
        self.verticalLayout_158 = QVBoxLayout(self.co2_6_group_2)
        self.verticalLayout_158.setObjectName(u"verticalLayout_158")
        self.co2_6_normal_radio_2 = QRadioButton(self.co2_6_group_2)
        self.co2_6_normal_radio_2.setObjectName(u"co2_6_normal_radio_2")
        self.co2_6_normal_radio_2.setChecked(True)

        self.verticalLayout_158.addWidget(self.co2_6_normal_radio_2)

        self.co2_6_crc_radio_2 = QRadioButton(self.co2_6_group_2)
        self.co2_6_crc_radio_2.setObjectName(u"co2_6_crc_radio_2")

        self.verticalLayout_158.addWidget(self.co2_6_crc_radio_2)

        self.co2_6_timing_radio_2 = QRadioButton(self.co2_6_group_2)
        self.co2_6_timing_radio_2.setObjectName(u"co2_6_timing_radio_2")

        self.verticalLayout_158.addWidget(self.co2_6_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_6_group_2, 1, 1, 1, 1)

        self.co2_7_group_2 = QGroupBox(self.temperature_tab)
        self.co2_7_group_2.setObjectName(u"co2_7_group_2")
        self.co2_7_group_2.setCheckable(True)
        self.verticalLayout_157 = QVBoxLayout(self.co2_7_group_2)
        self.verticalLayout_157.setObjectName(u"verticalLayout_157")
        self.co2_7_normal_radio_2 = QRadioButton(self.co2_7_group_2)
        self.co2_7_normal_radio_2.setObjectName(u"co2_7_normal_radio_2")
        self.co2_7_normal_radio_2.setChecked(True)

        self.verticalLayout_157.addWidget(self.co2_7_normal_radio_2)

        self.co2_7_crc_radio_2 = QRadioButton(self.co2_7_group_2)
        self.co2_7_crc_radio_2.setObjectName(u"co2_7_crc_radio_2")

        self.verticalLayout_157.addWidget(self.co2_7_crc_radio_2)

        self.co2_7_timing_radio_2 = QRadioButton(self.co2_7_group_2)
        self.co2_7_timing_radio_2.setObjectName(u"co2_7_timing_radio_2")

        self.verticalLayout_157.addWidget(self.co2_7_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_7_group_2, 1, 2, 1, 1)

        self.co2_8_group_2 = QGroupBox(self.temperature_tab)
        self.co2_8_group_2.setObjectName(u"co2_8_group_2")
        self.co2_8_group_2.setCheckable(True)
        self.verticalLayout_154 = QVBoxLayout(self.co2_8_group_2)
        self.verticalLayout_154.setObjectName(u"verticalLayout_154")
        self.co2_8_normal_radio_2 = QRadioButton(self.co2_8_group_2)
        self.co2_8_normal_radio_2.setObjectName(u"co2_8_normal_radio_2")
        self.co2_8_normal_radio_2.setChecked(True)

        self.verticalLayout_154.addWidget(self.co2_8_normal_radio_2)

        self.co2_8_crc_radio_2 = QRadioButton(self.co2_8_group_2)
        self.co2_8_crc_radio_2.setObjectName(u"co2_8_crc_radio_2")

        self.verticalLayout_154.addWidget(self.co2_8_crc_radio_2)

        self.co2_8_timing_radio_2 = QRadioButton(self.co2_8_group_2)
        self.co2_8_timing_radio_2.setObjectName(u"co2_8_timing_radio_2")

        self.verticalLayout_154.addWidget(self.co2_8_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_8_group_2, 1, 3, 1, 1)

        self.co2_9_group_2 = QGroupBox(self.temperature_tab)
        self.co2_9_group_2.setObjectName(u"co2_9_group_2")
        self.co2_9_group_2.setCheckable(True)
        self.verticalLayout_156 = QVBoxLayout(self.co2_9_group_2)
        self.verticalLayout_156.setObjectName(u"verticalLayout_156")
        self.co2_9_normal_radio_2 = QRadioButton(self.co2_9_group_2)
        self.co2_9_normal_radio_2.setObjectName(u"co2_9_normal_radio_2")
        self.co2_9_normal_radio_2.setChecked(True)

        self.verticalLayout_156.addWidget(self.co2_9_normal_radio_2)

        self.co2_9_crc_radio_2 = QRadioButton(self.co2_9_group_2)
        self.co2_9_crc_radio_2.setObjectName(u"co2_9_crc_radio_2")

        self.verticalLayout_156.addWidget(self.co2_9_crc_radio_2)

        self.co2_9_timing_radio_2 = QRadioButton(self.co2_9_group_2)
        self.co2_9_timing_radio_2.setObjectName(u"co2_9_timing_radio_2")

        self.verticalLayout_156.addWidget(self.co2_9_timing_radio_2)


        self.gridLayout_6.addWidget(self.co2_9_group_2, 1, 4, 1, 1)

        self.device_tab.addTab(self.temperature_tab, "")
        self.solar_tab = QWidget()
        self.solar_tab.setObjectName(u"solar_tab")
        self.gridLayout_7 = QGridLayout(self.solar_tab)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.co2_0_group_3 = QGroupBox(self.solar_tab)
        self.co2_0_group_3.setObjectName(u"co2_0_group_3")
        self.co2_0_group_3.setCheckable(True)
        self.verticalLayout_161 = QVBoxLayout(self.co2_0_group_3)
        self.verticalLayout_161.setObjectName(u"verticalLayout_161")
        self.co2_0_normal_radio_3 = QRadioButton(self.co2_0_group_3)
        self.co2_0_normal_radio_3.setObjectName(u"co2_0_normal_radio_3")
        self.co2_0_normal_radio_3.setChecked(True)

        self.verticalLayout_161.addWidget(self.co2_0_normal_radio_3)

        self.co2_0_crc_radio_3 = QRadioButton(self.co2_0_group_3)
        self.co2_0_crc_radio_3.setObjectName(u"co2_0_crc_radio_3")

        self.verticalLayout_161.addWidget(self.co2_0_crc_radio_3)

        self.co2_0_timing_radio_3 = QRadioButton(self.co2_0_group_3)
        self.co2_0_timing_radio_3.setObjectName(u"co2_0_timing_radio_3")

        self.verticalLayout_161.addWidget(self.co2_0_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_0_group_3, 0, 0, 1, 1)

        self.co2_1_group_3 = QGroupBox(self.solar_tab)
        self.co2_1_group_3.setObjectName(u"co2_1_group_3")
        self.co2_1_group_3.setCheckable(True)
        self.verticalLayout_169 = QVBoxLayout(self.co2_1_group_3)
        self.verticalLayout_169.setObjectName(u"verticalLayout_169")
        self.co2_1_normal_radio_3 = QRadioButton(self.co2_1_group_3)
        self.co2_1_normal_radio_3.setObjectName(u"co2_1_normal_radio_3")
        self.co2_1_normal_radio_3.setChecked(True)

        self.verticalLayout_169.addWidget(self.co2_1_normal_radio_3)

        self.co2_1_crc_radio_3 = QRadioButton(self.co2_1_group_3)
        self.co2_1_crc_radio_3.setObjectName(u"co2_1_crc_radio_3")

        self.verticalLayout_169.addWidget(self.co2_1_crc_radio_3)

        self.co2_1_timing_radio_3 = QRadioButton(self.co2_1_group_3)
        self.co2_1_timing_radio_3.setObjectName(u"co2_1_timing_radio_3")

        self.verticalLayout_169.addWidget(self.co2_1_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_1_group_3, 0, 1, 1, 1)

        self.co2_2_group_3 = QGroupBox(self.solar_tab)
        self.co2_2_group_3.setObjectName(u"co2_2_group_3")
        self.co2_2_group_3.setCheckable(True)
        self.verticalLayout_162 = QVBoxLayout(self.co2_2_group_3)
        self.verticalLayout_162.setObjectName(u"verticalLayout_162")
        self.co2_2_normal_radio_3 = QRadioButton(self.co2_2_group_3)
        self.co2_2_normal_radio_3.setObjectName(u"co2_2_normal_radio_3")
        self.co2_2_normal_radio_3.setChecked(True)

        self.verticalLayout_162.addWidget(self.co2_2_normal_radio_3)

        self.co2_2_crc_radio_3 = QRadioButton(self.co2_2_group_3)
        self.co2_2_crc_radio_3.setObjectName(u"co2_2_crc_radio_3")

        self.verticalLayout_162.addWidget(self.co2_2_crc_radio_3)

        self.co2_2_timing_radio_3 = QRadioButton(self.co2_2_group_3)
        self.co2_2_timing_radio_3.setObjectName(u"co2_2_timing_radio_3")

        self.verticalLayout_162.addWidget(self.co2_2_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_2_group_3, 0, 2, 1, 1)

        self.co2_3_group_3 = QGroupBox(self.solar_tab)
        self.co2_3_group_3.setObjectName(u"co2_3_group_3")
        self.co2_3_group_3.setCheckable(True)
        self.verticalLayout_170 = QVBoxLayout(self.co2_3_group_3)
        self.verticalLayout_170.setObjectName(u"verticalLayout_170")
        self.co2_3_normal_radio_3 = QRadioButton(self.co2_3_group_3)
        self.co2_3_normal_radio_3.setObjectName(u"co2_3_normal_radio_3")
        self.co2_3_normal_radio_3.setChecked(True)

        self.verticalLayout_170.addWidget(self.co2_3_normal_radio_3)

        self.co2_3_crc_radio_3 = QRadioButton(self.co2_3_group_3)
        self.co2_3_crc_radio_3.setObjectName(u"co2_3_crc_radio_3")

        self.verticalLayout_170.addWidget(self.co2_3_crc_radio_3)

        self.co2_3_timing_radio_3 = QRadioButton(self.co2_3_group_3)
        self.co2_3_timing_radio_3.setObjectName(u"co2_3_timing_radio_3")

        self.verticalLayout_170.addWidget(self.co2_3_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_3_group_3, 0, 3, 1, 1)

        self.co2_4_group_3 = QGroupBox(self.solar_tab)
        self.co2_4_group_3.setObjectName(u"co2_4_group_3")
        self.co2_4_group_3.setCheckable(True)
        self.verticalLayout_165 = QVBoxLayout(self.co2_4_group_3)
        self.verticalLayout_165.setObjectName(u"verticalLayout_165")
        self.co2_4_normal_radio_3 = QRadioButton(self.co2_4_group_3)
        self.co2_4_normal_radio_3.setObjectName(u"co2_4_normal_radio_3")
        self.co2_4_normal_radio_3.setChecked(True)

        self.verticalLayout_165.addWidget(self.co2_4_normal_radio_3)

        self.co2_4_crc_radio_3 = QRadioButton(self.co2_4_group_3)
        self.co2_4_crc_radio_3.setObjectName(u"co2_4_crc_radio_3")

        self.verticalLayout_165.addWidget(self.co2_4_crc_radio_3)

        self.co2_4_timing_radio_3 = QRadioButton(self.co2_4_group_3)
        self.co2_4_timing_radio_3.setObjectName(u"co2_4_timing_radio_3")

        self.verticalLayout_165.addWidget(self.co2_4_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_4_group_3, 0, 4, 1, 1)

        self.co2_5_group_3 = QGroupBox(self.solar_tab)
        self.co2_5_group_3.setObjectName(u"co2_5_group_3")
        self.co2_5_group_3.setCheckable(True)
        self.verticalLayout_163 = QVBoxLayout(self.co2_5_group_3)
        self.verticalLayout_163.setObjectName(u"verticalLayout_163")
        self.co2_5_normal_radio_3 = QRadioButton(self.co2_5_group_3)
        self.co2_5_normal_radio_3.setObjectName(u"co2_5_normal_radio_3")
        self.co2_5_normal_radio_3.setChecked(True)

        self.verticalLayout_163.addWidget(self.co2_5_normal_radio_3)

        self.co2_5_crc_radio_3 = QRadioButton(self.co2_5_group_3)
        self.co2_5_crc_radio_3.setObjectName(u"co2_5_crc_radio_3")

        self.verticalLayout_163.addWidget(self.co2_5_crc_radio_3)

        self.co2_5_timing_radio_3 = QRadioButton(self.co2_5_group_3)
        self.co2_5_timing_radio_3.setObjectName(u"co2_5_timing_radio_3")

        self.verticalLayout_163.addWidget(self.co2_5_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_5_group_3, 1, 0, 1, 1)

        self.co2_6_group_3 = QGroupBox(self.solar_tab)
        self.co2_6_group_3.setObjectName(u"co2_6_group_3")
        self.co2_6_group_3.setCheckable(True)
        self.verticalLayout_168 = QVBoxLayout(self.co2_6_group_3)
        self.verticalLayout_168.setObjectName(u"verticalLayout_168")
        self.co2_6_normal_radio_3 = QRadioButton(self.co2_6_group_3)
        self.co2_6_normal_radio_3.setObjectName(u"co2_6_normal_radio_3")
        self.co2_6_normal_radio_3.setChecked(True)

        self.verticalLayout_168.addWidget(self.co2_6_normal_radio_3)

        self.co2_6_crc_radio_3 = QRadioButton(self.co2_6_group_3)
        self.co2_6_crc_radio_3.setObjectName(u"co2_6_crc_radio_3")

        self.verticalLayout_168.addWidget(self.co2_6_crc_radio_3)

        self.co2_6_timing_radio_3 = QRadioButton(self.co2_6_group_3)
        self.co2_6_timing_radio_3.setObjectName(u"co2_6_timing_radio_3")

        self.verticalLayout_168.addWidget(self.co2_6_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_6_group_3, 1, 1, 1, 1)

        self.co2_7_group_3 = QGroupBox(self.solar_tab)
        self.co2_7_group_3.setObjectName(u"co2_7_group_3")
        self.co2_7_group_3.setCheckable(True)
        self.verticalLayout_167 = QVBoxLayout(self.co2_7_group_3)
        self.verticalLayout_167.setObjectName(u"verticalLayout_167")
        self.co2_7_normal_radio_3 = QRadioButton(self.co2_7_group_3)
        self.co2_7_normal_radio_3.setObjectName(u"co2_7_normal_radio_3")
        self.co2_7_normal_radio_3.setChecked(True)

        self.verticalLayout_167.addWidget(self.co2_7_normal_radio_3)

        self.co2_7_crc_radio_3 = QRadioButton(self.co2_7_group_3)
        self.co2_7_crc_radio_3.setObjectName(u"co2_7_crc_radio_3")

        self.verticalLayout_167.addWidget(self.co2_7_crc_radio_3)

        self.co2_7_timing_radio_3 = QRadioButton(self.co2_7_group_3)
        self.co2_7_timing_radio_3.setObjectName(u"co2_7_timing_radio_3")

        self.verticalLayout_167.addWidget(self.co2_7_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_7_group_3, 1, 2, 1, 1)

        self.co2_8_group_3 = QGroupBox(self.solar_tab)
        self.co2_8_group_3.setObjectName(u"co2_8_group_3")
        self.co2_8_group_3.setCheckable(True)
        self.verticalLayout_164 = QVBoxLayout(self.co2_8_group_3)
        self.verticalLayout_164.setObjectName(u"verticalLayout_164")
        self.co2_8_normal_radio_3 = QRadioButton(self.co2_8_group_3)
        self.co2_8_normal_radio_3.setObjectName(u"co2_8_normal_radio_3")
        self.co2_8_normal_radio_3.setChecked(True)

        self.verticalLayout_164.addWidget(self.co2_8_normal_radio_3)

        self.co2_8_crc_radio_3 = QRadioButton(self.co2_8_group_3)
        self.co2_8_crc_radio_3.setObjectName(u"co2_8_crc_radio_3")

        self.verticalLayout_164.addWidget(self.co2_8_crc_radio_3)

        self.co2_8_timing_radio_3 = QRadioButton(self.co2_8_group_3)
        self.co2_8_timing_radio_3.setObjectName(u"co2_8_timing_radio_3")

        self.verticalLayout_164.addWidget(self.co2_8_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_8_group_3, 1, 3, 1, 1)

        self.co2_9_group_3 = QGroupBox(self.solar_tab)
        self.co2_9_group_3.setObjectName(u"co2_9_group_3")
        self.co2_9_group_3.setCheckable(True)
        self.verticalLayout_166 = QVBoxLayout(self.co2_9_group_3)
        self.verticalLayout_166.setObjectName(u"verticalLayout_166")
        self.co2_9_normal_radio_3 = QRadioButton(self.co2_9_group_3)
        self.co2_9_normal_radio_3.setObjectName(u"co2_9_normal_radio_3")
        self.co2_9_normal_radio_3.setChecked(True)

        self.verticalLayout_166.addWidget(self.co2_9_normal_radio_3)

        self.co2_9_crc_radio_3 = QRadioButton(self.co2_9_group_3)
        self.co2_9_crc_radio_3.setObjectName(u"co2_9_crc_radio_3")

        self.verticalLayout_166.addWidget(self.co2_9_crc_radio_3)

        self.co2_9_timing_radio_3 = QRadioButton(self.co2_9_group_3)
        self.co2_9_timing_radio_3.setObjectName(u"co2_9_timing_radio_3")

        self.verticalLayout_166.addWidget(self.co2_9_timing_radio_3)


        self.gridLayout_7.addWidget(self.co2_9_group_3, 1, 4, 1, 1)

        self.device_tab.addTab(self.solar_tab, "")
        self.motor_tab = QWidget()
        self.motor_tab.setObjectName(u"motor_tab")
        self.gridLayout_8 = QGridLayout(self.motor_tab)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.co2_0_group_4 = QGroupBox(self.motor_tab)
        self.co2_0_group_4.setObjectName(u"co2_0_group_4")
        self.co2_0_group_4.setCheckable(True)
        self.verticalLayout_171 = QVBoxLayout(self.co2_0_group_4)
        self.verticalLayout_171.setObjectName(u"verticalLayout_171")
        self.co2_0_normal_radio_4 = QRadioButton(self.co2_0_group_4)
        self.co2_0_normal_radio_4.setObjectName(u"co2_0_normal_radio_4")
        self.co2_0_normal_radio_4.setChecked(True)

        self.verticalLayout_171.addWidget(self.co2_0_normal_radio_4)

        self.co2_0_crc_radio_4 = QRadioButton(self.co2_0_group_4)
        self.co2_0_crc_radio_4.setObjectName(u"co2_0_crc_radio_4")

        self.verticalLayout_171.addWidget(self.co2_0_crc_radio_4)

        self.co2_0_timing_radio_4 = QRadioButton(self.co2_0_group_4)
        self.co2_0_timing_radio_4.setObjectName(u"co2_0_timing_radio_4")

        self.verticalLayout_171.addWidget(self.co2_0_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_0_group_4, 0, 0, 1, 1)

        self.co2_1_group_4 = QGroupBox(self.motor_tab)
        self.co2_1_group_4.setObjectName(u"co2_1_group_4")
        self.co2_1_group_4.setCheckable(True)
        self.verticalLayout_179 = QVBoxLayout(self.co2_1_group_4)
        self.verticalLayout_179.setObjectName(u"verticalLayout_179")
        self.co2_1_normal_radio_4 = QRadioButton(self.co2_1_group_4)
        self.co2_1_normal_radio_4.setObjectName(u"co2_1_normal_radio_4")
        self.co2_1_normal_radio_4.setChecked(True)

        self.verticalLayout_179.addWidget(self.co2_1_normal_radio_4)

        self.co2_1_crc_radio_4 = QRadioButton(self.co2_1_group_4)
        self.co2_1_crc_radio_4.setObjectName(u"co2_1_crc_radio_4")

        self.verticalLayout_179.addWidget(self.co2_1_crc_radio_4)

        self.co2_1_timing_radio_4 = QRadioButton(self.co2_1_group_4)
        self.co2_1_timing_radio_4.setObjectName(u"co2_1_timing_radio_4")

        self.verticalLayout_179.addWidget(self.co2_1_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_1_group_4, 0, 1, 1, 1)

        self.co2_2_group_4 = QGroupBox(self.motor_tab)
        self.co2_2_group_4.setObjectName(u"co2_2_group_4")
        self.co2_2_group_4.setCheckable(True)
        self.verticalLayout_172 = QVBoxLayout(self.co2_2_group_4)
        self.verticalLayout_172.setObjectName(u"verticalLayout_172")
        self.co2_2_normal_radio_4 = QRadioButton(self.co2_2_group_4)
        self.co2_2_normal_radio_4.setObjectName(u"co2_2_normal_radio_4")
        self.co2_2_normal_radio_4.setChecked(True)

        self.verticalLayout_172.addWidget(self.co2_2_normal_radio_4)

        self.co2_2_crc_radio_4 = QRadioButton(self.co2_2_group_4)
        self.co2_2_crc_radio_4.setObjectName(u"co2_2_crc_radio_4")

        self.verticalLayout_172.addWidget(self.co2_2_crc_radio_4)

        self.co2_2_timing_radio_4 = QRadioButton(self.co2_2_group_4)
        self.co2_2_timing_radio_4.setObjectName(u"co2_2_timing_radio_4")

        self.verticalLayout_172.addWidget(self.co2_2_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_2_group_4, 0, 2, 1, 1)

        self.co2_3_group_4 = QGroupBox(self.motor_tab)
        self.co2_3_group_4.setObjectName(u"co2_3_group_4")
        self.co2_3_group_4.setCheckable(True)
        self.verticalLayout_180 = QVBoxLayout(self.co2_3_group_4)
        self.verticalLayout_180.setObjectName(u"verticalLayout_180")
        self.co2_3_normal_radio_4 = QRadioButton(self.co2_3_group_4)
        self.co2_3_normal_radio_4.setObjectName(u"co2_3_normal_radio_4")
        self.co2_3_normal_radio_4.setChecked(True)

        self.verticalLayout_180.addWidget(self.co2_3_normal_radio_4)

        self.co2_3_crc_radio_4 = QRadioButton(self.co2_3_group_4)
        self.co2_3_crc_radio_4.setObjectName(u"co2_3_crc_radio_4")

        self.verticalLayout_180.addWidget(self.co2_3_crc_radio_4)

        self.co2_3_timing_radio_4 = QRadioButton(self.co2_3_group_4)
        self.co2_3_timing_radio_4.setObjectName(u"co2_3_timing_radio_4")

        self.verticalLayout_180.addWidget(self.co2_3_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_3_group_4, 0, 3, 1, 1)

        self.co2_4_group_4 = QGroupBox(self.motor_tab)
        self.co2_4_group_4.setObjectName(u"co2_4_group_4")
        self.co2_4_group_4.setCheckable(True)
        self.verticalLayout_175 = QVBoxLayout(self.co2_4_group_4)
        self.verticalLayout_175.setObjectName(u"verticalLayout_175")
        self.co2_4_normal_radio_4 = QRadioButton(self.co2_4_group_4)
        self.co2_4_normal_radio_4.setObjectName(u"co2_4_normal_radio_4")
        self.co2_4_normal_radio_4.setChecked(True)

        self.verticalLayout_175.addWidget(self.co2_4_normal_radio_4)

        self.co2_4_crc_radio_4 = QRadioButton(self.co2_4_group_4)
        self.co2_4_crc_radio_4.setObjectName(u"co2_4_crc_radio_4")

        self.verticalLayout_175.addWidget(self.co2_4_crc_radio_4)

        self.co2_4_timing_radio_4 = QRadioButton(self.co2_4_group_4)
        self.co2_4_timing_radio_4.setObjectName(u"co2_4_timing_radio_4")

        self.verticalLayout_175.addWidget(self.co2_4_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_4_group_4, 0, 4, 1, 1)

        self.co2_5_group_4 = QGroupBox(self.motor_tab)
        self.co2_5_group_4.setObjectName(u"co2_5_group_4")
        self.co2_5_group_4.setCheckable(True)
        self.verticalLayout_173 = QVBoxLayout(self.co2_5_group_4)
        self.verticalLayout_173.setObjectName(u"verticalLayout_173")
        self.co2_5_normal_radio_4 = QRadioButton(self.co2_5_group_4)
        self.co2_5_normal_radio_4.setObjectName(u"co2_5_normal_radio_4")
        self.co2_5_normal_radio_4.setChecked(True)

        self.verticalLayout_173.addWidget(self.co2_5_normal_radio_4)

        self.co2_5_crc_radio_4 = QRadioButton(self.co2_5_group_4)
        self.co2_5_crc_radio_4.setObjectName(u"co2_5_crc_radio_4")

        self.verticalLayout_173.addWidget(self.co2_5_crc_radio_4)

        self.co2_5_timing_radio_4 = QRadioButton(self.co2_5_group_4)
        self.co2_5_timing_radio_4.setObjectName(u"co2_5_timing_radio_4")

        self.verticalLayout_173.addWidget(self.co2_5_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_5_group_4, 1, 0, 1, 1)

        self.co2_6_group_4 = QGroupBox(self.motor_tab)
        self.co2_6_group_4.setObjectName(u"co2_6_group_4")
        self.co2_6_group_4.setCheckable(True)
        self.verticalLayout_178 = QVBoxLayout(self.co2_6_group_4)
        self.verticalLayout_178.setObjectName(u"verticalLayout_178")
        self.co2_6_normal_radio_4 = QRadioButton(self.co2_6_group_4)
        self.co2_6_normal_radio_4.setObjectName(u"co2_6_normal_radio_4")
        self.co2_6_normal_radio_4.setChecked(True)

        self.verticalLayout_178.addWidget(self.co2_6_normal_radio_4)

        self.co2_6_crc_radio_4 = QRadioButton(self.co2_6_group_4)
        self.co2_6_crc_radio_4.setObjectName(u"co2_6_crc_radio_4")

        self.verticalLayout_178.addWidget(self.co2_6_crc_radio_4)

        self.co2_6_timing_radio_4 = QRadioButton(self.co2_6_group_4)
        self.co2_6_timing_radio_4.setObjectName(u"co2_6_timing_radio_4")

        self.verticalLayout_178.addWidget(self.co2_6_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_6_group_4, 1, 1, 1, 1)

        self.co2_7_group_4 = QGroupBox(self.motor_tab)
        self.co2_7_group_4.setObjectName(u"co2_7_group_4")
        self.co2_7_group_4.setCheckable(True)
        self.verticalLayout_177 = QVBoxLayout(self.co2_7_group_4)
        self.verticalLayout_177.setObjectName(u"verticalLayout_177")
        self.co2_7_normal_radio_4 = QRadioButton(self.co2_7_group_4)
        self.co2_7_normal_radio_4.setObjectName(u"co2_7_normal_radio_4")
        self.co2_7_normal_radio_4.setChecked(True)

        self.verticalLayout_177.addWidget(self.co2_7_normal_radio_4)

        self.co2_7_crc_radio_4 = QRadioButton(self.co2_7_group_4)
        self.co2_7_crc_radio_4.setObjectName(u"co2_7_crc_radio_4")

        self.verticalLayout_177.addWidget(self.co2_7_crc_radio_4)

        self.co2_7_timing_radio_4 = QRadioButton(self.co2_7_group_4)
        self.co2_7_timing_radio_4.setObjectName(u"co2_7_timing_radio_4")

        self.verticalLayout_177.addWidget(self.co2_7_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_7_group_4, 1, 2, 1, 1)

        self.co2_8_group_4 = QGroupBox(self.motor_tab)
        self.co2_8_group_4.setObjectName(u"co2_8_group_4")
        self.co2_8_group_4.setCheckable(True)
        self.verticalLayout_174 = QVBoxLayout(self.co2_8_group_4)
        self.verticalLayout_174.setObjectName(u"verticalLayout_174")
        self.co2_8_normal_radio_4 = QRadioButton(self.co2_8_group_4)
        self.co2_8_normal_radio_4.setObjectName(u"co2_8_normal_radio_4")
        self.co2_8_normal_radio_4.setChecked(True)

        self.verticalLayout_174.addWidget(self.co2_8_normal_radio_4)

        self.co2_8_crc_radio_4 = QRadioButton(self.co2_8_group_4)
        self.co2_8_crc_radio_4.setObjectName(u"co2_8_crc_radio_4")

        self.verticalLayout_174.addWidget(self.co2_8_crc_radio_4)

        self.co2_8_timing_radio_4 = QRadioButton(self.co2_8_group_4)
        self.co2_8_timing_radio_4.setObjectName(u"co2_8_timing_radio_4")

        self.verticalLayout_174.addWidget(self.co2_8_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_8_group_4, 1, 3, 1, 1)

        self.co2_9_group_4 = QGroupBox(self.motor_tab)
        self.co2_9_group_4.setObjectName(u"co2_9_group_4")
        self.co2_9_group_4.setCheckable(True)
        self.verticalLayout_176 = QVBoxLayout(self.co2_9_group_4)
        self.verticalLayout_176.setObjectName(u"verticalLayout_176")
        self.co2_9_normal_radio_4 = QRadioButton(self.co2_9_group_4)
        self.co2_9_normal_radio_4.setObjectName(u"co2_9_normal_radio_4")
        self.co2_9_normal_radio_4.setChecked(True)

        self.verticalLayout_176.addWidget(self.co2_9_normal_radio_4)

        self.co2_9_crc_radio_4 = QRadioButton(self.co2_9_group_4)
        self.co2_9_crc_radio_4.setObjectName(u"co2_9_crc_radio_4")

        self.verticalLayout_176.addWidget(self.co2_9_crc_radio_4)

        self.co2_9_timing_radio_4 = QRadioButton(self.co2_9_group_4)
        self.co2_9_timing_radio_4.setObjectName(u"co2_9_timing_radio_4")

        self.verticalLayout_176.addWidget(self.co2_9_timing_radio_4)


        self.gridLayout_8.addWidget(self.co2_9_group_4, 1, 4, 1, 1)

        self.device_tab.addTab(self.motor_tab, "")

        self.gridLayout_15.addWidget(self.device_tab, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.device_group, 1, 0, 1, 3)

        self.log_group = QGroupBox(self.centralwidget)
        self.log_group.setObjectName(u"log_group")
        self.gridLayout = QGridLayout(self.log_group)
        self.gridLayout.setObjectName(u"gridLayout")
        
        self.log_clear_btn = QPushButton(" Log 삭제 ")
        self.log_clear_btn.setObjectName(u"log_clear_btn")
        self.log_clear_btn.setMaximumHeight(35)
        
        self.log_text_edit = QPlainTextEdit(self.log_group)
        self.log_text_edit.setObjectName(u"log_text_edit")
        self.log_text_edit.setEnabled(True)
        font1 = QFont()
        font1.setPointSize(12)
        self.log_text_edit.setFont(font1)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setCenterOnScroll(False)

        self.gridLayout.addWidget(self.log_clear_btn, 0, 0)
        self.gridLayout.addWidget(self.log_text_edit, 1, 0)


        self.gridLayout_2.addWidget(self.log_group, 2, 0, 1, 3)

        self.settings_group = QGroupBox(self.centralwidget)
        self.settings_group.setObjectName(u"settings_group")
        self.gridLayout_14 = QGridLayout(self.settings_group)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.timing_delay_spin = QSpinBox(self.settings_group)
        self.timing_delay_spin.setObjectName(u"timing_delay_spin")
        self.timing_delay_spin.setMaximum(5000)
        self.timing_delay_spin.setSingleStep(1)
        self.timing_delay_spin.setValue(500)

        self.gridLayout_14.addWidget(self.timing_delay_spin, 0, 1, 1, 1)

        self.label_2 = QLabel(self.settings_group)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_14.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.settings_group, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 644, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.baudrate_combo.setCurrentIndex(4)
        self.device_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", f"근로복지공단 DAQ Slave 테스트 프로그램_V5 (251106)", None))
        self.com_group.setTitle(QCoreApplication.translate("MainWindow", u"Com", None))
        self.baudrate_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"9600", None))
        self.baudrate_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"19200", None))
        self.baudrate_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"38400", None))
        self.baudrate_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"57600", None))
        self.baudrate_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"115200", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"COM", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Baudrate", None))
        self.com_open_btn.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.com_close_btn.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.device_group.setTitle(QCoreApplication.translate("MainWindow", u"\uc7a5\uce58 \ubcc4 \uc751\ub2f5 \uc120\ud0dd", None))
        self.tag1p2w_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.tag1p2w_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.tag1p2w_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.tag1p2w_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.tag1p2w_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.tag1p2w_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.tag1p2w_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.tag1p2w_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.tag1p2w_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.tag1p2w_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag1p2w_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.tag1p2w_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag1p2w_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag1p2w_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.tag1p2w_tab), QCoreApplication.translate("MainWindow", u"\ub2e8\uc0c1", None))
        self.tag3p3w_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.tag3p3w_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.tag3p3w_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.tag3p3w_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.tag3p3w_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.tag3p3w_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.tag3p3w_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.tag3p3w_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.tag3p3w_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.tag3p3w_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p3w_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.tag3p3w_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p3w_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p3w_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.tag3p3w_tab), QCoreApplication.translate("MainWindow", u"3\uc0c13\uc120", None))
        self.tag3p4w_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.tag3p4w_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.tag3p4w_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.tag3p4w_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.tag3p4w_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.tag3p4w_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.tag3p4w_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.tag3p4w_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.tag3p4w_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.tag3p4w_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.tag3p4w_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.tag3p4w_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.tag3p4w_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.tag3p4w_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.tag3p4w_tab), QCoreApplication.translate("MainWindow", u"3\uc0c14\uc120", None))
        self.oil_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.oil_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.oil_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.oil_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.oil_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.oil_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.oil_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.oil_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.oil_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.oil_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.oil_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.oil_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.oil_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.oil_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.oil_tab), QCoreApplication.translate("MainWindow", u"\uc720\ub7c9", None))
        self.water_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.water_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.water_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.water_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.water_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.water_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.water_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.water_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.water_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.water_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.water_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.water_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.water_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.water_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.water_tab), QCoreApplication.translate("MainWindow", u"\uc218\ub3c4", None))
        self.co2_0_group.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.co2_0_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_0_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_0_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_1_group.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.co2_1_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_1_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_1_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_2_group.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.co2_2_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_2_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_2_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_3_group.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.co2_3_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_3_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_3_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_4_group.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.co2_4_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_4_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_4_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_5_group.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.co2_5_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_5_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_5_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_6_group.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.co2_6_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_6_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_6_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_7_group.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.co2_7_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_7_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_7_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_8_group.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.co2_8_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_8_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_8_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_9_group.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.co2_9_normal_radio.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_9_crc_radio.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_9_timing_radio.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.co2_tab), QCoreApplication.translate("MainWindow", u"CO2", None))
        self.co2_0_group_2.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.co2_0_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_0_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_0_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_1_group_2.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.co2_1_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_1_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_1_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_2_group_2.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.co2_2_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_2_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_2_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_3_group_2.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.co2_3_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_3_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_3_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_4_group_2.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.co2_4_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_4_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_4_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_5_group_2.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.co2_5_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_5_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_5_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_6_group_2.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.co2_6_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_6_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_6_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_7_group_2.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.co2_7_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_7_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_7_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_8_group_2.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.co2_8_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_8_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_8_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_9_group_2.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.co2_9_normal_radio_2.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_9_crc_radio_2.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_9_timing_radio_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.temperature_tab), QCoreApplication.translate("MainWindow", u"\uc628\uc2b5\ub3c4", None))
        self.co2_0_group_3.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.co2_0_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_0_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_0_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_1_group_3.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.co2_1_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_1_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_1_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_2_group_3.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.co2_2_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_2_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_2_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_3_group_3.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.co2_3_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_3_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_3_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_4_group_3.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.co2_4_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_4_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_4_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_5_group_3.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.co2_5_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_5_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_5_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_6_group_3.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.co2_6_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_6_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_6_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_7_group_3.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.co2_7_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_7_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_7_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_8_group_3.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.co2_8_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_8_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_8_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_9_group_3.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.co2_9_normal_radio_3.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_9_crc_radio_3.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_9_timing_radio_3.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.solar_tab), QCoreApplication.translate("MainWindow", u"\uc77c\uc0ac\ub7c9", None))
        self.co2_0_group_4.setTitle(QCoreApplication.translate("MainWindow", u"0\ubc88", None))
        self.co2_0_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_0_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_0_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_1_group_4.setTitle(QCoreApplication.translate("MainWindow", u"1\ubc88", None))
        self.co2_1_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_1_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_1_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_2_group_4.setTitle(QCoreApplication.translate("MainWindow", u"2\ubc88", None))
        self.co2_2_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_2_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_2_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_3_group_4.setTitle(QCoreApplication.translate("MainWindow", u"3\ubc88", None))
        self.co2_3_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_3_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_3_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_4_group_4.setTitle(QCoreApplication.translate("MainWindow", u"4\ubc88", None))
        self.co2_4_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_4_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_4_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_5_group_4.setTitle(QCoreApplication.translate("MainWindow", u"5\ubc88", None))
        self.co2_5_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_5_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_5_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_6_group_4.setTitle(QCoreApplication.translate("MainWindow", u"6\ubc88", None))
        self.co2_6_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_6_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_6_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_7_group_4.setTitle(QCoreApplication.translate("MainWindow", u"7\ubc88", None))
        self.co2_7_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_7_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_7_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_8_group_4.setTitle(QCoreApplication.translate("MainWindow", u"8\ubc88", None))
        self.co2_8_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_8_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_8_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.co2_9_group_4.setTitle(QCoreApplication.translate("MainWindow", u"9\ubc88", None))
        self.co2_9_normal_radio_4.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc0c1", None))
        self.co2_9_crc_radio_4.setText(QCoreApplication.translate("MainWindow", u"CRC \uc5d0\ub7ec", None))
        self.co2_9_timing_radio_4.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec", None))
        self.device_tab.setTabText(self.device_tab.indexOf(self.motor_tab), QCoreApplication.translate("MainWindow", u"DC\ubaa8\ud130", None))
        self.log_group.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.settings_group.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ud0c0\uc774\ubc0d \uc5d0\ub7ec Delay(ms)", None))
    # retranslateUi

