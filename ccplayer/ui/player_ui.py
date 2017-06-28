# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created: Wed Jun 28 14:19:51 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setFixedSize(259, 513)
        self.open_icon = QtGui.QIcon("../icons/open")
        self.delete_icon = QtGui.QIcon("../icons/delete")
        self.rewind_icon = QtGui.QIcon("../icons/rewind")
        self.play_icon = QtGui.QIcon("../icons/play")
        self.pause_icon = QtGui.QIcon("../icons/pause")
        self.terminate_icon = QtGui.QIcon('../icons/terminate')
        self.next_icon = QtGui.QIcon("../icons/next")
        self.simplify_icon = QtGui.QIcon('../icons/simplify')
        self.seek_slider = phonon.Phonon.SeekSlider(Dialog)
        self.seek_slider.setGeometry(QtCore.QRect(10, 30, 241, 19))
        self.seek_slider.setObjectName(_fromUtf8("seek_slider"))
        self.name_label = QtGui.QLabel(Dialog)
        self.name_label.setGeometry(QtCore.QRect(10, 10, 201, 16))
        self.name_label.setText(_fromUtf8(""))
        self.name_label.setObjectName(_fromUtf8("name_label"))
        self.play_button = QtGui.QPushButton(Dialog)
        self.play_button.setGeometry(QtCore.QRect(90, 70, 31, 31))
        self.play_button.setText(_fromUtf8(""))
        self.play_button.setIcon(self.pause_icon)
        self.play_button.setObjectName(_fromUtf8("play_button"))
        self.terminate_button = QtGui.QPushButton(Dialog)
        self.terminate_button.setGeometry(QtCore.QRect(120, 70, 31, 31))
        self.terminate_button.setText(_fromUtf8(""))
        self.terminate_button.setIcon(self.terminate_icon)
        self.terminate_button.setObjectName(_fromUtf8("terminate_button"))
        self.rewind_button = QtGui.QPushButton(Dialog)
        self.rewind_button.setGeometry(QtCore.QRect(60, 70, 31, 31))
        self.rewind_button.setText(_fromUtf8(""))
        self.rewind_button.setIcon(self.rewind_icon)
        self.rewind_button.setObjectName(_fromUtf8("rewind_button"))
        self.volume_slider = phonon.Phonon.VolumeSlider(Dialog)
        self.volume_slider.setGeometry(QtCore.QRect(180, 80, 71, 22))
        self.volume_slider.setObjectName(_fromUtf8("volume_slider"))
        self.open_button = QtGui.QPushButton(Dialog)
        self.open_button.setGeometry(QtCore.QRect(10, 450, 31, 31))
        self.open_button.setText(_fromUtf8(""))
        self.open_button.setIcon(self.open_icon)
        self.open_button.setObjectName(_fromUtf8("open_button"))
        self.next_button = QtGui.QPushButton(Dialog)
        self.next_button.setGeometry(QtCore.QRect(150, 70, 31, 31))
        self.next_button.setText(_fromUtf8(""))
        self.next_button.setIcon(self.next_icon)
        self.next_button.setObjectName(_fromUtf8("next_button"))
        self.delete_button = QtGui.QPushButton(Dialog)
        self.delete_button.setGeometry(QtCore.QRect(40, 450, 31, 31))
        self.delete_button.setText(_fromUtf8(""))
        self.delete_button.setIcon(self.delete_icon)
        self.delete_button.setObjectName(_fromUtf8("delete_button"))
        self.simplify_button = QtGui.QPushButton(Dialog)
        self.simplify_button.setGeometry(QtCore.QRect(70, 450, 31, 31))
        self.simplify_button.setText(_fromUtf8(""))
        self.simplify_button.setIcon(self.simplify_icon)
        self.simplify_button.setAutoDefault(True)
        self.simplify_button.setObjectName(_fromUtf8("simplify_button"))
        self.mode_combobox = QtGui.QComboBox(Dialog)
        self.mode_combobox.setGeometry(QtCore.QRect(10, 80, 51, 20))
        self.mode_combobox.setObjectName(_fromUtf8("mode_combobox"))
        self.mode_combobox.addItem(_fromUtf8(""))
        self.mode_combobox.addItem(_fromUtf8(""))
        self.mode_combobox.addItem(_fromUtf8(""))
        self.now_time_label = QtGui.QLabel(Dialog)
        self.now_time_label.setGeometry(QtCore.QRect(10, 50, 41, 16))
        self.now_time_label.setText(_fromUtf8(""))
        self.now_time_label.setObjectName(_fromUtf8("now_time_label"))
        self.end_time_label = QtGui.QLabel(Dialog)
        self.end_time_label.setGeometry(QtCore.QRect(210, 50, 41, 16))
        self.end_time_label.setText(_fromUtf8(""))
        self.end_time_label.setObjectName(_fromUtf8("end_time_label"))
        self.table_widget = QtGui.QTableWidget(Dialog)
        self.table_widget.setGeometry(QtCore.QRect(10, 110, 241, 331))
        self.table_widget.setObjectName(_fromUtf8("table_widget"))
        self.table_widget.setColumnCount(2)

        self.table_widget.setHorizontalHeaderLabels([u'歌名', u'时长'])
        self.table_widget.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        # self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.table_widget.setShowGrid(False)
        self.table_widget.setColumnWidth(0, 110)
        self.table_widget.setColumnWidth(1, 110)

        self.lyric_label = QtGui.QLabel(Dialog)
        self.lyric_label.setGeometry(QtCore.QRect(10, 490, 231, 16))
        self.lyric_label.setText(_fromUtf8(""))
        self.lyric_label.setObjectName(_fromUtf8("lyric_label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "CC Player", None))
        self.now_time_label.setText('00:00')
        self.end_time_label.setText('00:00')
        self.mode_combobox.setItemText(0, _translate("Dialog", "顺序", None))
        self.mode_combobox.setItemText(1, _translate("Dialog", "循环", None))
        self.mode_combobox.setItemText(2, _translate("Dialog", "随机", None))

from PyQt4 import phonon
