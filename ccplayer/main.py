# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys

from PyQt4 import QtGui

from ccplayer.logistic.player import Player

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myqq = Player()
    sys.exit(app.exec_())
