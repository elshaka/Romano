# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sun Aug  5 23:17:59 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(250, 293)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setMinimumSize(QtCore.QSize(250, 0))
        Login.setMaximumSize(QtCore.QSize(250, 365))
        self.verticalLayout = QtGui.QVBoxLayout(Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(Login)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.logoLabel = QtGui.QLabel(Login)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap(":/icons/romano-icon.png"))
        self.logoLabel.setScaledContents(False)
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.verticalLayout.addWidget(self.logoLabel)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.usernameLineEdit = QtGui.QLineEdit(Login)
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.usernameLineEdit)
        self.label = QtGui.QLabel(Login)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(Login)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.passwordLineEdit = QtGui.QLineEdit(Login)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginButton = QtGui.QPushButton(Login)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayout.addWidget(self.loginButton)
        self.exitButton = QtGui.QPushButton(Login)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtGui.QApplication.translate("Login", "Romano - Iniciar sesión", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Login", "Romano", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Login", "Usuario", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Login", "Contraseña", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("Login", "Iniciar sesión", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("Login", "Salir", None, QtGui.QApplication.UnicodeUTF8))

import pixmaps_rc
