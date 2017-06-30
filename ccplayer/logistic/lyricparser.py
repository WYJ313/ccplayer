# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re

class LyricParser:
    def __init__(self):
        self.res = {}

    def loads(self, fileName):
        with open(fileName, 'r') as f:
            for line in f.readlines():
                m = re.match('(\[\d{2}:\d{2}\.\d{2}\])(.+)', line)
                if m is not None:
                    tmp = m.group()
                    i = tmp.find('.')
                    key = tmp[1: i].strip()
                    j = tmp.find(']')
                    value = tmp[j+1:].strip()
                    self.res[key] = value

    def dumps(self):
        return self.res

if __name__ == '__main__':
    lp = LyricParser()
    f = u'./musics/晴天.lrc'
    lp.loads(f)
    for key in lp.dumps():
        print(key)
        print(lp.dumps()[key].decode('utf-8'))
