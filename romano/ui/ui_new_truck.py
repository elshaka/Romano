# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_truck.ui'
#
# Created: Mon Aug  6 14:10:53 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewTruck(object):
    def setupUi(self, NewTruck):
        NewTruck.setObjectName("NewTruck")
        NewTruck.resize(400, 130)
        self.verticalLayout = QtGui.QVBoxLayout(NewTruck)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(NewTruck)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.licensePlateLineEdit = QtGui.QLineEdit(NewTruck)
        self.licensePlateLineEdit.setObjectName("licensePlateLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.licensePlateLineEdit)
        self.label_2 = QtGui.QLabel(NewTruck)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.carriersComboBox = QtGui.QComboBox(NewTruck)
        self.carriersComboBox.setEditable(True)
        self.carriersComboBox.setObjectName("carriersComboBox")
        self.horizontalLayout.addWidget(self.carriersComboBox)
        self.addCarrierButton = QtGui.QToolButton(NewTruck)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/add-transaction.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addCarrierButton.setIcon(icon)
        self.addCarrierButton.setObjectName("addCarrierButton")
        self.horizontalLayout.addWidget(self.addCarrierButton)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(NewTruck)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.createTruckButton = QtGui.QPushButton(NewTruck)
        self.createTruckButton.setObjectName("createTruckButton")
        self.horizontalLayout_2.addWidget(self.createTruckButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(NewTruck)
        QtCore.QMetaObject.connectSlotsByName(NewTruck)

    def retranslateUi(self, NewTruck):
        NewTruck.setWindowTitle(QtGui.QApplication.translate("NewTruck", "Nuevo camión", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewTruck", "Placa", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewTruck", "Transportista", None, QtGui.QApplication.UnicodeUTF8))
        self.addCarrierButton.setText(QtGui.QApplication.translate("NewTruck", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("NewTruck", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.createTruckButton.setText(QtGui.QApplication.translate("NewTruck", "Crear camión", None, QtGui.QApplication.UnicodeUTF8))

import pixmaps_rc
