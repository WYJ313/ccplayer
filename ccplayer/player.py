# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys, os

from PyQt4 import QtGui, QtCore
from player_ui import Ui_Dialog
from PyQt4 import phonon
from PyQt4.phonon import Phonon

import logging
import random

from lyricparser import LyricParser

logging.basicConfig(level=logging.DEBUG)

ON = 1
OFF = 0

class UItest(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        QtGui.QWidget.__init__(self, parent)
        self.file = ''
        self.audio_path = ''
        self.media_source = None
        self.ui = None
        self.sources = []
        self.index = -1
        self.lyric = {}
        self.simplify = OFF

        self.media_obj = phonon.Phonon.MediaObject(self)
        self.audio_sink = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.audio_path = Phonon.createPath(self.media_obj, self.audio_sink)

        self.loginGui()

        self.load_config()
        self.mode = unicode(self.ui.mode_combobox.currentText())
        self._connect()

    def loginGui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.seek_slider.setMediaObject(self.media_obj)
        self.ui.volume_slider.setAudioOutput(self.audio_sink)

        self.show()

    def _connect(self):
        self.connect(self.ui.open_button, QtCore.SIGNAL('clicked()'),
                     self.open_clicked)
        self.connect(self.ui.delete_button, QtCore.SIGNAL('clicked()'),
                     self.delete_clicked)
        self.connect(self.ui.play_button, QtCore.SIGNAL('clicked()'),
                     self.play_clicked)
        self.connect(self.ui.terminate_button, QtCore.SIGNAL('clicked()'),
                     self.terminate_clicked_twice)
        self.connect(self.ui.rewind_button, QtCore.SIGNAL('clicked()'),
                     self.rewind_clicked)
        self.connect(self.ui.next_button, QtCore.SIGNAL('clicked()'),
                     self.next_clicked)
        self.media_obj.tick.connect(self.set_now)
        self.media_obj.tick.connect(self.set_lyric)
        self.media_obj.aboutToFinish.connect(self.next_track)
        self.connect(self.ui.mode_combobox, QtCore.SIGNAL('activated(QString)'),
                     self.order)
        self.ui.table_widget.verticalHeader().sectionDoubleClicked\
            .connect(self.versection_clicked)
        self.connect(self.ui.simplify_button, QtCore.SIGNAL('clicked()'),
                     self.simplify_button_clicked)
        self.media_obj.totalTimeChanged.connect(self.change_end_time)

    def change_end_time(self):
        if self.state == ON:
            self.ui.end_time_label.setText('%02d:%02d'% \
                            (self.set_time(self.media_obj.totalTime())))
            rows = self.ui.table_widget.rowCount()
            if rows + 1 == len(self.sources):
                self.ui.table_widget.setRowCount(len(self.sources))                                 # 这里开始创建
                name = QtGui.QTableWidgetItem(self.file.split('\\')[-1].split('.')[0])
                self.ui.table_widget.setItem(self.index, 0, name)
                time = QtGui.QTableWidgetItem( '%02d:%02d'% \
                                      (self.set_time(self.media_obj.totalTime())))
                self.ui.table_widget.setItem(self.index, 1, time)


    def simplify_button_clicked(self):
        if self.simplify == OFF:
            self.setFixedSize(259, 110)
            self.ui.open_button.move(190, 0)
            self.ui.simplify_button.move(220, 0)
            self.simplify = ON
        elif self.simplify == ON:
            self.setFixedSize(259, 513)
            self.ui.open_button.move(10, 450)
            self.ui.simplify_button.move(70,450)
            self.simplify = OFF
        else:
            logging.debug('精简模式出现异常')

    def delete_clicked(self):
        rows = self.ui.table_widget.selectedIndexes()
        delete_list = []
        for r in rows:
            if r.row() not in delete_list:
                delete_list.append(r.row())
        delete_list.sort()

        if self.index in delete_list:
            count = 0
            count2 = 0
            for i in delete_list:
                if i < self.index:
                    count += 1
                del self.sources[i-count2]
                self.ui.table_widget.removeRow(i-count2)
                count2 += 1
            self.index -= count
            if len(self.sources) == 0:
                self.terminate_clicked_twice()
                return
            self.index %= len(self.sources)
            print('current index:'+str(self.index))
            self.file = self.sources[self.index]
            file = self.file
            self.state = ON
            if self.file:
                self.file = os.path.normpath(self.file)
                self.ui.end_time_label.setText(
                    self.ui.table_widget.item(self.index, 1).text())
                self.load_media()
                self.play_media()
                self.ui.name_label.setText(self.file.split('\\')[-1].split('.')[0])
                self.load_lyric()
                self.ui.play_button.setIcon(self.ui.play_icon)
            print(len(self.sources))
            if len(self.sources) > 0:
                pass
            else:
                self.terminate_clicked()
        else:
            count = 0
            count2 = 0
            for i in delete_list:
                if i < self.index:
                    count += 1
                del self.sources[i-count2]
                self.ui.table_widget.removeRow(i-count2)
                count2 += 1
            self.index -= count
        print('len source:'+str(len(self.sources)))
        print(self.index)

    def versection_clicked(self ,index):
        self.index = index
        print('clicked play:'+str(index))
        self.file = self.sources[index]
        file = self.file
        print(self.file.split('/')[-1].split('.')[0])
        self.state = ON
        if self.file:
            self.file = os.path.normpath(self.file)
            self.ui.end_time_label.setText(self.ui.table_widget.item(index, 1).text())
            self.load_media()
            self.play_media()
            self.ui.name_label.setText(self.file.split('\\')[-1].split('.')[0])
            self.load_lyric()
            self.ui.play_button.setIcon(self.ui.play_icon)

    def next_track(self):
        if self.mode == u'顺序':
            self.next_clicked()
        elif self.mode == u'循环':
            self.file = self.file
            self.load_media()
            self.play_media()
            self.load_lyric()
        elif self.mode == u'随机':
            self.random_play()

    def random_play(self):
        tmp = random.randint(0, len(self.sources)-1)
        self.index = tmp
        self.file = self.sources[tmp]
        self.file = os.path.normpath(self.file)
        self.load_media()
        self.play_media()
        self.load_lyric()
        self.ui.end_time_label.setText('%02d:%02d'%
                                (self.set_time(self.media_obj.totalTime())))

    # 获取播放方式的值
    def order(self, text):
        self.mode = text

    def set_lyric(self, time):
        m, s =self.set_time(time)
        key = '%02d:%02d'%(m,s)
        if self.lyric.has_key(key):
            self.ui.lyric_label.setText(self.lyric[key].decode('utf-8'))

    def set_now(self, time):
        m, s =self.set_time(time)
        self.ui.now_time_label.setText('%02d:%02d'%(m,s))

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
            self.load_lyric()
            self.ui.end_time_label.setText('%02d:%02d'%
                                  (self.set_time(self.media_obj.totalTime())))
        else:
            self.ui.name_label.setText(u'请先打开一个文件')

    def next_clicked(self):
        if self.media_source:
            self.index = (self.index +len(self.sources) + 1) % len(self.sources)
            self.file = self.sources[self.index]
            self.file = os.path.normpath(self.file)
            self.load_media()
            self.play_media()
            self.load_lyric()
            self.ui.end_time_label.setText('%02d:%02d'%
                                  (self.set_time(self.media_obj.totalTime())))
        else:
            self.ui.name_label.setText(u'请先打开一个文件')

    def terminate_clicked(self):
        if self.media_obj:
            self.media_obj.stop()
        self.media_source = None
        self.ui.play_button.setIcon(self.ui.pause_icon)
        self.ui.name_label.setText('')
        self.ui.now_time_label.setText('00:00')
        self.ui.end_time_label.setText('00:00')
        self.ui.lyric_label.setText('')
        self.ui.play_button.setIcon(self.ui.pause_icon)

    def terminate_clicked_twice(self):      # 这个方法主要是为了解决当terminate时，slider变化导致歌词没有清空的问题
        self.terminate_clicked()
        self.terminate_clicked()

    def open_clicked(self):
        logging.debug('open button clicked')
        self.file = ''
        self.file = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open Audio File',
                './musics/', 'MP3 file (*.mp3);;wav(*.wav);;'))
        logging.debug(self.file)

        if self.file:
            self.state = ON
            self.sources.append(self.file)
            self.index = len(self.sources) - 1
            self.file = os.path.normpath(self.file)
            self.load_media()
            self.play_media()
            self.load_lyric()

            self.ui.play_button.setIcon(self.ui.play_icon)

    def play_clicked(self):
        if self.media_source is None:
            self.ui.name_label.setText(u'请先打开一个文件')
            return

        if self.media_obj is None:
            self.ui.name_label.setText(u"文件格式错误")
            return

        if self.state == ON:
            self.media_obj.pause()
            self.state = OFF
            self.ui.play_button.setIcon(self.ui.pause_icon)
        else:
            self.media_obj.play()
            self.state = ON
            self.ui.play_button.setIcon(self.ui.play_icon)

    def load_media(self):
        self.state = ON
        self.media_source = phonon.Phonon.MediaSource(self.file)
        self.media_obj.setCurrentSource(self.media_source)


    def load_lyric(self):
        try:
            lp = LyricParser()
            f = self.sources[self.index].replace('.mp3', '.lrc')
            lp.loads(f)
            self.lyric = lp.dumps()
        except:
            logging.debug('没有发现歌词')

    def play_media(self):
        if self.state == ON:
            self.media_obj.play()
            self.ui.name_label.setText(self.file.split('\\')[-1])

    def closeEvent(self, QCloseEvent):
        with open('./configs/sources.config', 'w') as output:
            output.write(';'.join(self.sources))

        with open('./configs/table_widget.config', 'w') as output:
            rows = self.ui.table_widget.rowCount()
            cols = self.ui.table_widget.columnCount()
            lst = []
            for i in range(rows):
                tmp = []
                for j in range(cols):
                    tmp.append(str(self.ui.table_widget.item(i, j).text()))
                s = ','.join(tmp)
                lst.append(s)
            output.write(';'.join(lst))


    def load_config(self):
         with open('./configs/sources.config', 'r') as input:
             lines = input.readline()
             if len(lines) == 0:
                 return
             for line in lines.split(';'):
                self.sources.append(line.decode('utf-8'))

         lst = []
         with open('./configs/table_widget.config', 'r') as input:
             lines = input.readline()
             if len(lines) == 0:
                 return
             for line in lines.split(';'):
                 tmp = []
                 for item in line.split(','):
                     tmp.append(item)
                 lst.append(tmp)
             self.ui.table_widget.setRowCount(len(self.sources))
             rows = self.ui.table_widget.rowCount()
             cols = self.ui.table_widget.columnCount()
             for i in range(rows):
                 for j in range(cols):
                     item = QtGui.QTableWidgetItem(lst[i][j].decode('utf-8'))
                     self.ui.table_widget.setItem(i, j, item)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myqq = UItest()
    sys.exit(app.exec_())
