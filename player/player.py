# -*- coding: utf-8 -*-
# !/usr/bin/env python


import sys, os

from PyQt4 import QtGui, QtCore
from PyQt4 import phonon
from PyQt4.phonon import Phonon
import logging
import random

logging.basicConfig(
    level=logging.DEBUG
)

ON = 1
OFF = 0


class Icon(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.file = ''
        self.audio_path = ''
        self.media_source = None
        self.ui = None
        self.sources = []
        self.index = -1

        self.media_obj = phonon.Phonon.MediaObject(self)
        self.audio_sink = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.audio_path = Phonon.createPath(self.media_obj, self.audio_sink)

        self._init_ui()
        self.mode = unicode(self.mode_combobox.currentText())
        self._connect()
        self.show()

    def _init_ui(self):
        self.setWindowTitle('CC Player')
        self.setWindowIcon(QtGui.QIcon('icons/cloud'))
        self.setFixedSize(300, 600)

        self.open_icon = QtGui.QIcon("/icons/open")
        self.delete_icon = QtGui.QIcon("/icons/delete")
        self.rewind_icon = QtGui.QIcon("icon/rewind")
        self.play_icon = QtGui.QIcon("icons/play")
        self.pause_icon = QtGui.QIcon("/icons/pause")
        self.terminate_icon = QtGui.QIcon('/icons/terminate')
        self.next_icon = QtGui.QIcon("/icons/next")

        self.open_button = QtGui.QPushButton(self)
        self.open_button.setFixedSize(30, 30)
        self.open_button.setIcon(self.open_icon)

        self.delete_button = QtGui.QPushButton(self)
        self.delete_button.setFixedSize(30, 30)
        self.delete_button.setIcon(self.open_icon)

        self.rewind_button = QtGui.QToolButton(self)
        self.rewind_button.setFixedSize(30, 30)
        self.rewind_button.setIcon(self.rewind_icon)

        self.play_button = QtGui.QPushButton(self)
        self.play_button.setFixedSize(30, 30)
        self.play_button.setIcon(self.play_icon)

        self.terminate_button = QtGui.QPushButton(self)
        self.terminate_button.setFixedSize(30, 30)
        self.terminate_button.setIcon(self.terminate_icon)

        self.next_button = QtGui.QToolButton(self)
        self.next_button.setFixedSize(30, 30)
        self.next_button.setIcon(self.next_icon)

        self.name_label = QtGui.QLabel('')
        self.name_label.setFixedSize(200, 20)
        self.seek_slider = Phonon.SeekSlider()
        self.seek_slider.setMediaObject(self.media_obj)
        self.volume_slider = phonon.Phonon.VolumeSlider()
        self.volume_slider.setAudioOutput(self.audio_sink)
        self.now_time_label = QtGui.QLabel('00:00')
        self.end_time_label = QtGui.QLabel('00:00')
        self.mode_combobox = QtGui.QComboBox(self)
        self.mode_combobox.addItem(u'顺序')
        self.mode_combobox.addItem(u'循环')
        self.mode_combobox.addItem(u'随机')

        self.table_widget = QtGui.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels([u'歌名', u'时长'])
        self.table_widget.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        #self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.table_widget.setShowGrid(False)
        self.table_widget.setColumnWidth(0, 115)
        self.table_widget.setColumnWidth(1, 115)
        self.table_widget.setColumnWidth(2, 50)
        self.table_widget.setColumnWidth(3, 50)

        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.seek_slider, 1, 0, 1, 10)
        grid.addWidget(self.now_time_label, 2, 0)
        grid.addWidget(self.end_time_label, 2, 1)
        grid.addWidget(self.mode_combobox, 3, 0)
        grid.addWidget(self.rewind_button, 3, 1)
        grid.addWidget(self.play_button, 3, 2)
        grid.addWidget(self.terminate_button, 3, 3)
        grid.addWidget(self.next_button, 3, 4)
        grid.addWidget(self.volume_slider, 4, 0)
        grid.addWidget(self.table_widget, 5, 0, 5, 10)
        grid.addWidget(self.open_button, 10, 0)
        grid.addWidget(self.delete_button, 10, 1)

        self.setLayout(grid)

    def _connect(self):
        self.connect(self.open_button, QtCore.SIGNAL('clicked()'),
                     self.open_clicked)
        self.connect(self.delete_button, QtCore.SIGNAL('clicked()'),
                     self.delete_clicked)
        self.connect(self.play_button, QtCore.SIGNAL('clicked()'),
                     self.play_clicked)
        self.connect(self.terminate_button, QtCore.SIGNAL('clicked()'),
                    self.terminate_clicked)
        self.connect(self.rewind_button, QtCore.SIGNAL('clicked()'),
                     self.rewind_clicked)
        self.connect(self.next_button, QtCore.SIGNAL('clicked()'),
                     self.next_clicked)
        self.media_obj.tick.connect(self.set_now)
        self.media_obj.aboutToFinish.connect(self.next_track)
        self.connect(self.mode_combobox, QtCore.SIGNAL('activated(QString)'),
                     self.order)
        self.table_widget.verticalHeader().sectionDoubleClicked\
            .connect(self.versection_clicked)

    def delete_clicked(self):
        rows = self.table_widget.selectedIndexes()
        delete_list = []
        for r in rows:
            if r.row() not in delete_list:
                delete_list.append(r.row())
        delete_list.sort()
        logging.debug(delete_list)
        logging.debug(self.index)
        logging.debug(len(self.sources))

        if self.index in delete_list:
            count = 0
            tmp = -1
            for i in delete_list:
                tmp += 1
                if i <= self.index:
                    count += 1
                del self.sources[i-tmp]
                self.table_widget.removeRow(i-tmp)
            self.index -= count
            if len(self.sources) > 0:
                pass
            else:
                self.terminate_clicked()
        else:
            count = 0
            for i in delete_list:
                if i < self.index:
                    count += 1
                del self.sources[i]
                self.table_widget.removeRow(i)
            self.index -= count
        print(self.index)


    def versection_clicked(self ,index):
        print(index)
        self.file = self.sources[index]
        self.state = ON
        if self.file:
            self.file = os.path.normpath(self.file)
            self.name_label.setText(self.table_widget.item(index, 0).text())
            self.end_time_label.setText(self.table_widget.item(index, 1).text())
            self.load_media()
            self.play_media()

    def next_track(self):
        if self.mode == u'顺序':
            self.next_clicked()
        elif self.mode == u'循环':
            self.file = self.file
            self.load_media()
            self.play_media()
        elif self.mode == u'随机':
            self.random_play()

    def random_play(self):
        tmp = random.randint(0, len(self.sources)-1)
        self.index = tmp
        self.file = self.sources[tmp]
        self.file = os.path.normpath(self.file)
        self.load_media()
        self.play_media()
        self.end_time_label.setText('%02d:%02d'%
                                (self.set_time(self.media_obj.totalTime())))

    # 获取播放方式的值
    def order(self, text):
        self.mode = text

    def set_now(self, time):
        time = time/1000   #除以1000得到秒单位
        h = time/3600   #小时
        m = (time-3600*h) / 60  #分钟
        s = (time-3600*h-m*60)  #秒
        self.now_time_label.setText('%02d:%02d'%(m,s))

    def set_time(self, time):
        time = time/1000   #除以1000得到秒单位
        h = time/3600   #小时
        m = (time-3600*h) / 60  #分钟
        s = (time-3600*h-m*60)  #秒
        return m, s

    def rewind_clicked(self):
        if self.media_source:
            self.index = (self.index +len(self.sources) - 1) % len(self.sources)
            self.file = self.sources[self.index]
            self.file = os.path.normpath(self.file)
            self.load_media()
            self.play_media()
            self.end_time_label.setText('%02d:%02d'%
                                  (self.set_time(self.media_obj.totalTime())))
        else:
            self.name_label.setText(u'请先打开一个文件')

    def next_clicked(self):
        if self.media_source:
            self.index = (self.index +len(self.sources) + 1) % len(self.sources)
            self.file = self.sources[self.index]
            self.file = os.path.normpath(self.file)
            self.load_media()
            self.play_media()
            self.end_time_label.setText('%02d:%02d'%
                                  (self.set_time(self.media_obj.totalTime())))
        else:
            self.name_label.setText(u'请先打开一个文件')

    def terminate_clicked(self):
        if self.media_obj:
            self.media_obj.stop()
        self.media_source = None
        self.play_button.setIcon(self.play_icon)
        self.name_label.setText(u'')
        self.now_time_label.setText('00:00')
        self.end_time_label.setText('00:00')


    def open_clicked(self):
        self.file = ''
        logging.debug('open button clicked')
        self.file = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open Audio File',
                './musics/', 'MP3 file (*.mp3);;wav(*.wav);;'))

        if self.file:
            self.state = ON
            self.sources.append(self.file)
            self.index = len(self.sources) - 1
            self.table_widget.setRowCount(len(self.sources))
            name = QtGui.QTableWidgetItem(self.file.split('/')[-1].split('.')[0])
            self.table_widget.setItem(self.index, 0, name)
            self.file = os.path.normpath(self.file)
            self.load_media()
            self.play_media()
            self.end_time_label.setText('%02d:%02d'% \
                            (self.set_time(self.media_obj.totalTime())))      # 总是显示上一次时间，不知为何
            time = QtGui.QTableWidgetItem( '%02d:%02d'% \
                                      (self.set_time(self.media_obj.totalTime())))
            self.table_widget.setItem(self.index, 1, time)

    def play_clicked(self):
        if self.media_source is None:
            self.name_label.setText(u'请先打开一个文件')
            return

        if self.media_obj is None:
            self.name_label.setText(u"文件格式错误")
            return

        if self.state == ON:
            self.media_obj.pause()
            self.state = OFF
            self.play_button.setIcon(self.pause_icon)
        else:
            self.media_obj.play()
            self.state = ON
            self.play_button.setIcon(self.play_icon)

    def load_media(self):
        self.state = ON
        if self.media_source:
            del self.media_source
        self.media_source = phonon.Phonon.MediaSource(self.file)
        self.media_obj.setCurrentSource(self.media_source)

    def play_media(self):
        if self.state == ON:
            self.media_obj.play()
            self.name_label.setText(self.file.split('\\')[-1])


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    icon = Icon()
    icon.show()
    sys.exit(app.exec_())

