# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_ticket.ui'
#
# Created: Mon Jul 30 10:26:25 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewTicket(object):
    def setupUi(self, NewTicket):
        NewTicket.setObjectName("NewTicket")
        NewTicket.resize(480, 300)
        NewTicket.setMinimumSize(QtCore.QSize(480, 300))
        self.verticalLayout = QtGui.QVBoxLayout(NewTicket)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.driverLabel = QtGui.QLabel(NewTicket)
        self.driverLabel.setObjectName("driverLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.driverLabel)
        self.driversComboBox = QtGui.QComboBox(NewTicket)
        self.driversComboBox.setEditable(True)
        self.driversComboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.driversComboBox.setObjectName("driversComboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.driversComboBox)
        self.truckLabel = QtGui.QLabel(NewTicket)
        self.truckLabel.setObjectName("truckLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.truckLabel)
        self.trucksComboBox = QtGui.QComboBox(NewTicket)
        self.trucksComboBox.setEditable(True)
        self.trucksComboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.trucksComboBox.setObjectName("trucksComboBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.trucksComboBox)
        self.weightLabel = QtGui.QLabel(NewTicket)
        self.weightLabel.setObjectName("weightLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.weightLabel)
        self.weightLayout = QtGui.QHBoxLayout()
        self.weightLayout.setObjectName("weightLayout")
        self.incomingWeightSpinBox = QtGui.QDoubleSpinBox(NewTicket)
        self.incomingWeightSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.incomingWeightSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.incomingWeightSpinBox.setMaximum(999999.0)
        self.incomingWeightSpinBox.setObjectName("incomingWeightSpinBox")
        self.weightLayout.addWidget(self.incomingWeightSpinBox)
        self.captureWeightButton = QtGui.QPushButton(NewTicket)
        self.captureWeightButton.setMinimumSize(QtCore.QSize(120, 0))
        self.captureWeightButton.setCheckable(True)
        self.captureWeightButton.setChecked(False)
        self.captureWeightButton.setObjectName("captureWeightButton")
        self.weightLayout.addWidget(self.captureWeightButton)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.weightLayout)
        self.verticalLayout.addLayout(self.formLayout)
        self.label = QtGui.QLabel(NewTicket)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.commentTextEdit = QtGui.QTextEdit(NewTicket)
        self.commentTextEdit.setObjectName("commentTextEdit")
        self.verticalLayout.addWidget(self.commentTextEdit)
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(NewTicket)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonsLayout.addWidget(self.cancelButton)
        self.createTicketButton = QtGui.QPushButton(NewTicket)
        self.createTicketButton.setObjectName("createTicketButton")
        self.buttonsLayout.addWidget(self.createTicketButton)
        self.verticalLayout.addLayout(self.buttonsLayout)

        self.retranslateUi(NewTicket)
        QtCore.QMetaObject.connectSlotsByName(NewTicket)

    def retranslateUi(self, NewTicket):
        NewTicket.setWindowTitle(QtGui.QApplication.translate("NewTicket", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.driverLabel.setText(QtGui.QApplication.translate("NewTicket", "Chofer", None, QtGui.QApplication.UnicodeUTF8))
        self.truckLabel.setText(QtGui.QApplication.translate("NewTicket", "Camión", None, QtGui.QApplication.UnicodeUTF8))
        self.weightLabel.setText(QtGui.QApplication.translate("NewTicket", "Peso de entrada", None, QtGui.QApplication.UnicodeUTF8))
        self.incomingWeightSpinBox.setSuffix(QtGui.QApplication.translate("NewTicket", " Kg", None, QtGui.QApplication.UnicodeUTF8))
        self.captureWeightButton.setText(QtGui.QApplication.translate("NewTicket", "Capturar peso", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewTicket", "Comentario", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("NewTicket", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.createTicketButton.setText(QtGui.QApplication.translate("NewTicket", "Crear ticket", None, QtGui.QApplication.UnicodeUTF8))

