# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_driver.ui'
#
# Created: Fri Sep 25 07:22:31 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ChangeDriver(object):
    def setupUi(self, ChangeDriver):
        ChangeDriver.setObjectName("ChangeDriver")
        ChangeDriver.resize(413, 482)
        self.verticalLayout = QtGui.QVBoxLayout(ChangeDriver)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frequentWidget = QtGui.QWidget(ChangeDriver)
        self.frequentWidget.setObjectName("frequentWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frequentWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.frequentWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.filterLineEdit = QtGui.QLineEdit(self.frequentWidget)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.horizontalLayout_2.addWidget(self.filterLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.driversTableView = QtGui.QTableView(self.frequentWidget)
        self.driversTableView.setAlternatingRowColors(True)
        self.driversTableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.driversTableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.driversTableView.setObjectName("driversTableView")
        self.driversTableView.horizontalHeader().setHighlightSections(False)
        self.driversTableView.horizontalHeader().setStretchLastSection(True)
        self.driversTableView.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.driversTableView)
        self.verticalLayout.addWidget(self.frequentWidget)
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.changeButton = QtGui.QPushButton(ChangeDriver)
        self.changeButton.setObjectName("changeButton")
        self.buttonsLayout.addWidget(self.changeButton)
        self.cancelButton = QtGui.QPushButton(ChangeDriver)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonsLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.buttonsLayout)

        self.retranslateUi(ChangeDriver)
        QtCore.QMetaObject.connectSlotsByName(ChangeDriver)

    def retranslateUi(self, ChangeDriver):
        ChangeDriver.setWindowTitle(QtGui.QApplication.translate("ChangeDriver", "Cambiar chofer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ChangeDriver", "Filtrar", None, QtGui.QApplication.UnicodeUTF8))
        self.changeButton.setText(QtGui.QApplication.translate("ChangeDriver", "Cambiar", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ChangeDriver", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))

