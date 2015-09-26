# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_truck.ui'
#
# Created: Sat Sep 26 09:39:58 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ChangeTruck(object):
    def setupUi(self, ChangeTruck):
        ChangeTruck.setObjectName("ChangeTruck")
        ChangeTruck.resize(695, 482)
        self.verticalLayout = QtGui.QVBoxLayout(ChangeTruck)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frequentWidget = QtGui.QWidget(ChangeTruck)
        self.frequentWidget.setObjectName("frequentWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frequentWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.frequentWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.filterLineEdit = QtGui.QLineEdit(self.frequentWidget)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.horizontalLayout_2.addWidget(self.filterLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.trucksTableView = QtGui.QTableView(self.frequentWidget)
        self.trucksTableView.setAlternatingRowColors(True)
        self.trucksTableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.trucksTableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.trucksTableView.setObjectName("trucksTableView")
        self.trucksTableView.horizontalHeader().setHighlightSections(False)
        self.trucksTableView.horizontalHeader().setStretchLastSection(True)
        self.trucksTableView.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.trucksTableView)
        self.verticalLayout.addWidget(self.frequentWidget)
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.changeButton = QtGui.QPushButton(ChangeTruck)
        self.changeButton.setObjectName("changeButton")
        self.buttonsLayout.addWidget(self.changeButton)
        self.cancelButton = QtGui.QPushButton(ChangeTruck)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonsLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.buttonsLayout)

        self.retranslateUi(ChangeTruck)
        QtCore.QMetaObject.connectSlotsByName(ChangeTruck)

    def retranslateUi(self, ChangeTruck):
        ChangeTruck.setWindowTitle(QtGui.QApplication.translate("ChangeTruck", "Cambiar camión", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ChangeTruck", "Filtrar", None, QtGui.QApplication.UnicodeUTF8))
        self.changeButton.setText(QtGui.QApplication.translate("ChangeTruck", "Cambiar", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ChangeTruck", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))

from . import pixmaps_rc
