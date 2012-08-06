# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_new_carrier import Ui_NewCarrier
from mango.models.carrier import Carrier

class NewCarrier(QtGui.QDialog):
  def __init__(self, parent):
    super(NewCarrier, self).__init__(parent)
    self.api = parent.api
    self.ui = Ui_NewCarrier()
    self.ui.setupUi(self)
    
    self.ui.cancelButton.clicked.connect(self.reject)
    self.ui.createCarrierButton.clicked.connect(self.createCarrier)
    
  def createCarrier(self):
    code = self.ui.codeLineEdit.text()
    name = self.ui.nameLineEdit.text()
    rif = self.ui.rifLineEdit.text()
    email = self.ui.emailLineEdit.text()
    tel1 = self.ui.telLineEdit.text()
    address = self.ui.addressLineEdit.text()
    self.carrier = Carrier(code, name, rif)
    self.carrier.email = email
    self.carrier.tel1 = tel1
    self.carrier.address = address
    self.accept()
