# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import os
import random
import sys
import urllib2

from PyQt4 import QtGui, QtCore
from PyQt4 import phonon
from PyQt4.phonon import Phonon

from ccplayer.logistic.lyricparser import LyricParser
from ccplayer.ui.player_ui import Ui_Dialog

logging.basicConfig(level=logging.DEBUG)

ON = 1
OFF = 0

class Player(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        reload(sys)
        sys.setdefaultencoding(u'utf-8')
        QtGui.QWidget.__init__(self, parent)
        self.file = ''
        self.audioPath = ''
        self.mediaSource = None
        self.ui = None
        self.sources = []
        self.index = -1
        self.lyric = {}
        self.simplify = OFF
        self.state = OFF

        self.mediaObj = phonon.Phonon.MediaObject(self)
        self.audioSink = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.audioPath = Phonon.createPath(self.mediaObj, self.audioSink)

        self.loginGui()

        self.loadConfig()
        self.mode = unicode(self.ui.modeCombobox.currentText())
        self._connect()

    def loginGui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.seekSlider.setMediaObject(self.mediaObj)
        self.ui.volumeSlider.setAudioOutput(self.audioSink)

        self.show()

    def _connect(self):
        self.connect(self.ui.openButton, QtCore.SIGNAL('clicked()'),
                     self.openClicked)
        self.connect(self.ui.deleteButton, QtCore.SIGNAL('clicked()'),
                     self.deleteClicked)
        self.connect(self.ui.playButton, QtCore.SIGNAL('clicked()'),
                     self.playClicked)
        self.connect(self.ui.terminateButton, QtCore.SIGNAL('clicked()'),
                     self.terminateClickedTwice)
        self.connect(self.ui.rewindButton, QtCore.SIGNAL('clicked()'),
                     self.rewindClicked)
        self.connect(self.ui.nextButton, QtCore.SIGNAL('clicked()'),
                     self.nextClicked)
        self.mediaObj.tick.connect(self.setNow)
        self.mediaObj.tick.connect(self.setLyric)
        self.mediaObj.aboutToFinish.connect(self.nextTrack)
        self.connect(self.ui.modeCombobox, QtCore.SIGNAL('activated(QString)'),
                     self.order)
        self.ui.tableWidget.verticalHeader().sectionDoubleClicked\
            .connect(self.versectionClicked)
        self.connect(self.ui.simplifyButton, QtCore.SIGNAL('clicked()'),
                     self.simplifyButtonClicked)
        self.mediaObj.totalTimeChanged.connect(self.changeEndTime)


    def changeEndTime(self):
        if self.state == ON:
            self.ui.endTimeLabel.setText(u'%02d:%02d'% \
                            (self.setTime(self.mediaObj.totalTime())))
            rows = self.ui.tableWidget.rowCount()
            if rows + 1 == len(self.sources):
                self.ui.tableWidget.setRowCount(len(self.sources))                                 # 这里开始创建
                name = QtGui.QTableWidgetItem(self.file.split('\\')[-1].split('.')[0])
                self.ui.tableWidget.setItem(self.index, 0, name)
                time = QtGui.QTableWidgetItem(u'%02d:%02d'% \
                                      (self.setTime(self.mediaObj.totalTime())))
                self.ui.tableWidget.setItem(self.index, 1, time)

    def simplifyButtonClicked(self):
        if self.simplify == OFF:
            self.setFixedSize(259, 110)
            self.ui.openButton.move(190, 0)
            self.ui.simplifyButton.move(220, 0)
            self.simplify = ON
            logging.debug(u'简单模式开启')
        elif self.simplify == ON:
            self.setFixedSize(259, 513)
            self.ui.openButton.move(10, 450)
            self.ui.simplifyButton.move(70, 450)
            self.simplify = OFF
            logging.debug(u'简单模式关闭')
        else:
            raise RuntimeError(u'精简模式出现异常')

    def deleteClicked(self):
        rows = self.ui.tableWidget.selectedIndexes()
        deleteList = []
        for r in rows:
            if r.row() not in deleteList:
                deleteList.append(r.row())
        deleteList.sort()

        if self.index in deleteList:
            count = 0
            count2 = 0
            for i in deleteList:
                if i < self.index:
                    count += 1
                del self.sources[i-count2]
                logging.debug(u"从播放列表删除："+self.ui.tableWidget.item(i-count2, 0).text())
                self.ui.tableWidget.removeRow(i-count2)
                count2 += 1
            self.index -= count
            if len(self.sources) == 0:
                self.terminateClickedTwice()
                return
            self.index %= len(self.sources)     # 如果删除后列表不为空，则播放下一首
            self.file = self.sources[self.index]
            logging.debug(u'当前播放：'+self.file.split('/')[-1].split('.')[0])
            self.state = ON
            if self.file:
                self.file = os.path.normpath(self.file)
                self.ui.endTimeLabel.setText(
                    self.ui.tableWidget.item(self.index, 1).text())
                self.loadMedia()
                self.playMedia()
                self.ui.nameLabel.setText(self.file.split('\\')[-1].split('.')[0])
                self.loadLyric()
                self.ui.playButton.setIcon(self.ui.playIcon)
            if len(self.sources) > 0:
                pass
            else:
                self.terminateClicked()
        else:
            count = 0
            count2 = 0
            for i in deleteList:
                if i < self.index:
                    count += 1
                del self.sources[i-count2]
                logging.debug(u"从播放列表删除："+self.ui.tableWidget.item(i-count2, 0).text())
                self.ui.tableWidget.removeRow(i-count2)
                count2 += 1
            self.index -= count


    def versectionClicked(self ,index):
        self.index = index
        self.file = self.sources[index]
        logging.debug(u'当前播放：'+self.file.split('/')[-1].split('.')[0])
        self.state = ON
        if self.file:
            self.file = os.path.normpath(self.file)
            self.ui.endTimeLabel.setText(self.ui.tableWidget.item(index, 1).text())
            self.ui.nameLabel.setText(self.file.split('\\')[-1].split('.')[0])
            self.ui.playButton.setIcon(self.ui.playIcon)
            try:
                self.loadMedia()
                self.playMedia()
                self.loadLyric()
            except RuntimeError as e:
                raise e

    def nextTrack(self):
        if self.mode == u'顺序':
            self.nextClicked()
        elif self.mode == u'循环':
            self.file = self.file
            self.loadMedia()
            self.playMedia()
            self.loadLyric()
        elif self.mode == u'随机':
            self.randomPlay()

    def randomPlay(self):
        tmp = random.randint(0, len(self.sources)-1)
        self.index = tmp
        self.file = self.sources[tmp]
        logging.debug(u'当前播放：'+self.file.split('/')[-1].split('.')[0])
        self.file = os.path.normpath(self.file)
        self.loadMedia()
        self.playMedia()
        self.loadLyric()
        self.ui.endTimeLabel.setText(u'%02d:%02d'%
                                (self.setTime(self.mediaObj.totalTime())))

    # 获取播放方式的值
    def order(self, text):
        self.mode = text

    def setLyric(self, time):
        m, s =self.setTime(time)
        key = u'%02d:%02d'%(m,s)
        if self.lyric.has_key(key):
            self.ui.lyricLabel.setText(self.lyric[key].decode(u'utf-8'))

    def setNow(self, time):
        m, s =self.setTime(time)
        self.ui.nowTimeLabel.setText(u'%02d:%02d' % (m, s))

    def setTime(self, time):
        time = time/1000   #除以1000得到秒单位
        h = time/3600   #小时
        m = (time-3600*h) / 60  #分钟
        s = (time-3600*h-m*60)  #秒
        return m, s

    def rewindClicked(self):
        if self.mediaSource:
            if self.ui.modeCombobox.currentText() == u'随机':
                self.randomPlay()
            else:
                self.index = (self.index +len(self.sources) - 1) % len(self.sources)
                self.file = self.sources[self.index]
                logging.debug(u'当前播放：'+self.file.split('/')[-1].split('.')[0])
                self.file = os.path.normpath(self.file)
                self.loadMedia()
                self.playMedia()
                self.loadLyric()
                self.ui.endTimeLabel.setText(u'%02d:%02d' %
                                      (self.setTime(self.mediaObj.totalTime())))
        else:
            self.ui.nameLabel.setText(u'请先打开一个文件')

    def nextClicked(self):
        if self.mediaSource:
            if self.ui.modeCombobox.currentText() == u'随机':
                self.randomPlay()
            else:
                self.index = (self.index +len(self.sources) + 1) % len(self.sources)
                self.file = self.sources[self.index]
                logging.debug(u'当前播放：'+self.file.split('/')[-1].split('.')[0])
                self.file = os.path.normpath(self.file)
                self.loadMedia()
                self.playMedia()
                self.loadLyric()
                self.ui.endTimeLabel.setText(u'%02d:%02d' %
                                      (self.setTime(self.mediaObj.totalTime())))
        else:
            self.ui.nameLabel.setText(u'请先打开一个文件')

    def terminateClicked(self):
        if self.mediaObj:
            self.mediaObj.stop()
        self.mediaSource = None
        self.ui.playButton.setIcon(self.ui.pauseIcon)
        self.ui.nameLabel.setText('')
        self.ui.nowTimeLabel.setText(u'00:00')
        self.ui.endTimeLabel.setText(u'00:00')
        self.ui.lyricLabel.setText('')
        self.ui.playButton.setIcon(self.ui.pauseIcon)

    def terminateClickedTwice(self):      # 这个方法主要是为了解决当terminate时，slider变化导致歌词没有清空的问题
        self.terminateClicked()
        self.terminateClicked()
        logging.debug(u'终止状态')

    def openClicked(self):
        self.file = u''
        self.file = unicode(QtGui.QFileDialog.getOpenFileName(self, u'Open Audio File',
                u'./musics/', u'MP3 file (*.mp3);;wav(*.wav);;'))
        logging.debug(u'打开文件路径：'+self.file)
        suffix = self.file.split('\\')[-1].split('.')[-1]
        if suffix in [u'mp3', u'wav']:
            self.state = ON
            self.sources.append(self.file)
            self.index = len(self.sources) - 1
            self.file = os.path.normpath(self.file)
            self.loadMedia()
            self.playMedia()
            self.loadLyric()
            self.ui.playButton.setIcon(self.ui.playIcon)
        else:
            raise ValueError(u'不合法的音乐类型')

    def playClicked(self):
        if self.mediaSource is None:
            self.ui.nameLabel.setText(u'请先打开一个文件')
            return

        if self.mediaObj is None:
            self.ui.nameLabel.setText(u"文件格式错误")
            return

        if self.state == ON:
            self.mediaObj.pause()
            self.state = OFF
            self.ui.playButton.setIcon(self.ui.pauseIcon)
            logging.debug(u'暂停状态')
        else:
            self.mediaObj.play()
            self.state = ON
            self.ui.playButton.setIcon(self.ui.playIcon)
            logging.debug(u'播放状态')

    def loadMedia(self):
        self.state = ON
        self.mediaSource = phonon.Phonon.MediaSource(self.file)
        self.mediaObj.setCurrentSource(self.mediaSource)
        logging.debug(u'正在载入音乐文件')

    def loadLyric(self):
        try:
            lp = LyricParser()
            f = self.sources[self.index].replace(u'.mp3', u'.lrc')
            lp.loads(f)
            self.lyric = lp.dumps()
            logging.debug(u'正在载入歌词文件')
        except IOError as e:
            logging.error(u'没有发现歌词文件')
            raise e

    def playMedia(self):
        if self.state == ON:
            self.mediaObj.play()
            self.ui.nameLabel.setText(self.file.split('\\')[-1])
        else:
            raise RuntimeError


    def closeEvent(self, QCloseEvent):
        reply = QtGui.QMessageBox.question(self, u'提示',
                    u'是否最小化到托盘', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            QCloseEvent.ignore()
            self.setFixedSize(0, 0)
        else:
            QCloseEvent.accept()

        with open(u'./configs/sources.config', 'w') as output:
            output.write(';'.join(self.sources))

        with open(u'./configs/mode.config', 'w') as output:
            output.write(str(self.ui.modeCombobox.currentIndex()))

        with open(u'./configs/table_widget.config', 'w') as output:
            rows = self.ui.tableWidget.rowCount()
            cols = self.ui.tableWidget.columnCount()
            lst = []
            for i in range(rows):
                tmp = []
                for j in range(cols):
                    tmp.append(str(self.ui.tableWidget.item(i, j).text()))
                s = ','.join(tmp)
                lst.append(s)
            output.write(';'.join(lst))


    def loadConfig(self):
         with open(u'./configs/mode.config', 'r') as input:
             line = input.readline()
             self.ui.modeCombobox.setCurrentIndex(int(line))

         with open(u'./configs/sources.config', 'r') as input:
             lines = input.readline()
             if len(lines) == 0:
                 return
             for line in lines.split(';'):
                self.sources.append(line.decode(u'utf-8'))

         lst = []
         with open(u'./configs/table_widget.config', u'r') as input:
             lines = input.readline()
             if len(lines) == 0:
                 return
             for line in lines.split(';'):
                 tmp = []
                 for item in line.split(','):
                     tmp.append(item)
                 lst.append(tmp)
             self.ui.tableWidget.setRowCount(len(self.sources))
             rows = self.ui.tableWidget.rowCount()
             cols = self.ui.tableWidget.columnCount()
             for i in range(rows):
                 for j in range(cols):
                     item = QtGui.QTableWidgetItem(lst[i][j].decode(u'utf-8'))
                     self.ui.tableWidget.setItem(i, j, item)
         logging.debug(u'正在加载配置文件')

    def resize(self):
        self.setFixedSize(259, 513)

