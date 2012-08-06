# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_driver.ui'
#
# Created: Mon Aug  6 14:11:02 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewDriver(object):
    def setupUi(self, NewDriver):
        NewDriver.setObjectName("NewDriver")
        NewDriver.resize(363, 228)
        self.verticalLayout = QtGui.QVBoxLayout(NewDriver)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(NewDriver)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.nameLineEdit = QtGui.QLineEdit(NewDriver)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameLineEdit)
        self.label_2 = QtGui.QLabel(NewDriver)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.ciLineEdit = QtGui.QLineEdit(NewDriver)
        self.ciLineEdit.setObjectName("ciLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ciLineEdit)
        self.addressLineEdit = QtGui.QLineEdit(NewDriver)
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.addressLineEdit)
        self.label_3 = QtGui.QLabel(NewDriver)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(NewDriver)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.telLineEdit = QtGui.QLineEdit(NewDriver)
        self.telLineEdit.setObjectName("telLineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.telLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.label_5 = QtGui.QLabel(NewDriver)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(NewDriver)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.createDriverButton = QtGui.QPushButton(NewDriver)
        self.createDriverButton.setObjectName("createDriverButton")
        self.horizontalLayout.addWidget(self.createDriverButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewDriver)
        QtCore.QMetaObject.connectSlotsByName(NewDriver)

    def retranslateUi(self, NewDriver):
        NewDriver.setWindowTitle(QtGui.QApplication.translate("NewDriver", "Nuevo chofer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewDriver", "Nombre*", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewDriver", "Cédula*", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewDriver", "Dirección", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewDriver", "Teléfono", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("NewDriver", "*Campos obligatorios", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("NewDriver", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.createDriverButton.setText(QtGui.QApplication.translate("NewDriver", "Crear chofer", None, QtGui.QApplication.UnicodeUTF8))

