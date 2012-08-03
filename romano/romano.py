#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Romano
Author: Eleazar Meza (meza.eleazar@gmail.com)
"""

import sys
from PySide import QtGui
from ui.main import Main

def main():
  app = QtGui.QApplication(sys.argv)
  m = Main()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
