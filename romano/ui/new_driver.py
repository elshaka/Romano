# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_new_driver import Ui_NewDriver
from mango.models.driver import Driver

class NewDriver(QtGui.QDialog):
  def __init__(self, parent):
    super(NewDriver, self).__init__(parent)
    self.ui = Ui_NewDriver()
    self.ui.setupUi(self)
    
    self.ui.createDriverButton.clicked.connect(self.createDriver)
    self.ui.cancelButton.clicked.connect(self.reject)
    
  def createDriver(self):
    name = self.ui.nameLineEdit.text()
    ci = self.ui.ciLineEdit.text()
    address = self.ui.addressLineEdit.text()
    tel1 = self.ui.telLineEdit.text()
    tel2 = ""
    self.driver = Driver(ci, name, address, tel1, tel2)
    self.accept()
