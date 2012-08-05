# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_login import Ui_Login

class Login(QtGui.QDialog):
  def __init__(self, api, parent):
    super(Login, self).__init__(parent)
    self.ui = Ui_Login()
    self.ui.setupUi(self)
    self.setModal(True)
    self.api = api
    
    self.ui.loginButton.clicked.connect(self.login)
    self.ui.exitButton.clicked.connect(self.reject)
    self.api.loginFinished.connect(self.loginFinished)
    self.api.loginFailed.connect(self.loginFailed)
    
  def login(self):
    self.enabled = False
    username = self.ui.usernameLineEdit.text()
    password = self.ui.passwordLineEdit.text()
    self.api.login(username, password)
    
  def loginFinished(self, user):
    self.user = user
    self.accept()
    
  def loginFailed(self):
    msgBox = QtGui.QMessageBox()
    msgBox.setWindowTitle("Error")
    msgBox.setText(u"Credenciales inválidas")
    msgBox.exec_()
    self.enabled = True
