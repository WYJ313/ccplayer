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
        Dialog.setObjectName(_fromUtf8(u"Dialog"))
        Dialog.setFixedSize(259, 513)
        self.logoIcon = QtGui.QIcon(u'./icons/logo')
        self.openIcon = QtGui.QIcon(u"./icons/open")
        self.deleteIcon = QtGui.QIcon(u"./icons/delete")
        self.rewindIcon = QtGui.QIcon(u"./icons/rewind")
        self.playIcon = QtGui.QIcon(u"./icons/play")
        self.pauseIcon = QtGui.QIcon(u"./icons/pause")
        self.terminateIcon = QtGui.QIcon(u'./icons/terminate')
        self.nextIcon = QtGui.QIcon(u"./icons/next")
        self.simplifyIcon = QtGui.QIcon(u'./icons/simplify')
        self.downloadIcon = QtGui.QIcon(u'./icons/download')
        self.seekSlider = phonon.Phonon.SeekSlider(Dialog)
        self.seekSlider.setGeometry(QtCore.QRect(10, 30, 241, 19))
        self.seekSlider.setObjectName(_fromUtf8(u"seekSlider"))
        self.nameLabel = QtGui.QLabel(Dialog)
        self.nameLabel.setGeometry(QtCore.QRect(10, 10, 201, 16))
        self.nameLabel.setText(_fromUtf8(u""))
        self.nameLabel.setObjectName(_fromUtf8(u"nameLabel"))
        self.playButton = QtGui.QPushButton(Dialog)
        self.playButton.setGeometry(QtCore.QRect(90, 70, 31, 31))
        self.playButton.setText(_fromUtf8(u""))
        self.playButton.setToolTip(u'播放')
        self.playButton.setIcon(self.pauseIcon)
        self.playButton.setObjectName(_fromUtf8(u"playButton"))
        self.terminateButton = QtGui.QPushButton(Dialog)
        self.terminateButton.setGeometry(QtCore.QRect(120, 70, 31, 31))
        self.terminateButton.setText(_fromUtf8(u""))
        self.terminateButton.setToolTip(u'停止')
        self.terminateButton.setIcon(self.terminateIcon)
        self.terminateButton.setObjectName(_fromUtf8(u"terminateButton"))
        self.rewindButton = QtGui.QPushButton(Dialog)
        self.rewindButton.setGeometry(QtCore.QRect(60, 70, 31, 31))
        self.rewindButton.setText(_fromUtf8(u""))
        self.rewindButton.setToolTip(u'上一首')
        self.rewindButton.setIcon(self.rewindIcon)
        self.rewindButton.setObjectName(_fromUtf8(u"rewindButton"))
        self.volumeSlider = phonon.Phonon.VolumeSlider(Dialog)
        self.volumeSlider.setGeometry(QtCore.QRect(180, 80, 71, 22))
        self.volumeSlider.setObjectName(_fromUtf8(u"volumeSlider"))
        self.openButton = QtGui.QPushButton(Dialog)
        self.openButton.setGeometry(QtCore.QRect(10, 450, 31, 31))
        self.openButton.setText(_fromUtf8(u""))
        self.openButton.setToolTip(u'打开文件')
        self.openButton.setIcon(self.openIcon)
        self.openButton.setObjectName(_fromUtf8(u"openButton"))
        self.nextButton = QtGui.QPushButton(Dialog)
        self.nextButton.setGeometry(QtCore.QRect(150, 70, 31, 31))
        self.nextButton.setText(_fromUtf8(u""))
        self.nextButton.setToolTip(u'下一首')
        self.nextButton.setIcon(self.nextIcon)
        self.nextButton.setObjectName(_fromUtf8(u"nextButton"))
        self.deleteButton = QtGui.QPushButton(Dialog)
        self.deleteButton.setGeometry(QtCore.QRect(40, 450, 31, 31))
        self.deleteButton.setText(_fromUtf8(u""))
        self.deleteButton.setToolTip(u'删除')
        self.deleteButton.setIcon(self.deleteIcon)
        self.deleteButton.setObjectName(_fromUtf8(u"deleteButton"))
        self.simplifyButton = QtGui.QPushButton(Dialog)
        self.simplifyButton.setGeometry(QtCore.QRect(70, 450, 31, 31))
        self.simplifyButton.setText(_fromUtf8(u""))
        self.simplifyButton.setToolTip(u'简单模式')
        self.simplifyButton.setIcon(self.simplifyIcon)
        self.simplifyButton.setAutoDefault(True)
        self.simplifyButton.setObjectName(_fromUtf8(u"simplifyButton"))
        self.modeCombobox = QtGui.QComboBox(Dialog)
        self.modeCombobox.setGeometry(QtCore.QRect(10, 80, 51, 20))
        self.modeCombobox.setObjectName(_fromUtf8(u"modeCombobox"))
        self.modeCombobox.addItem(_fromUtf8(u""))
        self.modeCombobox.addItem(_fromUtf8(u""))
        self.modeCombobox.addItem(_fromUtf8(u""))
        self.nowTimeLabel = QtGui.QLabel(Dialog)
        self.nowTimeLabel.setGeometry(QtCore.QRect(10, 50, 41, 16))
        self.nowTimeLabel.setText(_fromUtf8(""))
        self.nowTimeLabel.setObjectName(_fromUtf8(u"nowTimeLabel"))
        self.endTimeLabel = QtGui.QLabel(Dialog)
        self.endTimeLabel.setGeometry(QtCore.QRect(210, 50, 41, 16))
        self.endTimeLabel.setText(_fromUtf8(""))
        self.endTimeLabel.setObjectName(_fromUtf8(u"endTimeLabel"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 241, 331))
        self.tableWidget.setObjectName(_fromUtf8(u"tableWidget"))
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderLabels([u'歌名', u'时长'])
        self.tableWidget.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        # self.table_widget.verticalHeader().setVisible(False)
        palette = QtGui.QPalette(self)
        palette.setColor(self.tableWidget.backgroundRole(), QtGui.QColor(255, 255, 255))   # 因为表头会继承背景颜色，所以把它调成白色
        self.tableWidget.verticalHeader().setPalette(palette)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.setColumnWidth(1, 110)

        self.lyricLabel = QtGui.QLabel(Dialog)
        self.lyricLabel.setGeometry(QtCore.QRect(10, 490, 231, 16))
        self.lyricLabel.setText(_fromUtf8(""))
        self.lyricLabel.setObjectName(_fromUtf8(u"lyric_label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate(u"Dialog", u"CC Player", None))
        Dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        Dialog.setWindowIcon(self.logoIcon)
        palette = QtGui.QPalette(self)
        palette.setColor(Dialog.backgroundRole(), QtGui.QColor(0, 206, 209))   # 设置背景颜色
        #palette1.setBrush(Dialog.backgroundRole(),
        #                  QtGui.QBrush(QtGui.QPixmap('../icons/background.jpg')))   # 设置背景图片
        Dialog.setPalette(palette)
        Dialog.setAutoFillBackground(True) # 不设置也可以
        self.nowTimeLabel.setText(u'00:00')
        self.endTimeLabel.setText(u'00:00')
        self.modeCombobox.setItemText(0, _translate(u"Dialog", u"顺序", None))
        self.modeCombobox.setItemText(1, _translate(u"Dialog", u"循环", None))
        self.modeCombobox.setItemText(2, _translate(u"Dialog", u"随机", None))
        self.tray = QtGui.QSystemTrayIcon(Dialog)
        self.tray.setIcon(self.logoIcon)
        self.trayMenu = QtGui.QMenu(Dialog)
        self.tray.show()
        self.aboutAction = QtGui.QAction(u"&显示", Dialog,
                                        triggered=Dialog.resize)
        self.quitAction = QtGui.QAction(u"&退出", Dialog,
                                        triggered=QtGui.qApp.quit)
        self.trayMenu = QtGui.QMenu(Dialog)
        self.trayMenu.addAction(self.aboutAction)
        self.trayMenu.addAction(self.quitAction)
        self.tray.setContextMenu(self.trayMenu)

from PyQt4 import phonon
