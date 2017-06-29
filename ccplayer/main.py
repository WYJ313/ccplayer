# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys, os
from PyQt4 import QtGui

from player import UItest



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myqq = UItest()
    sys.exit(app.exec_())
