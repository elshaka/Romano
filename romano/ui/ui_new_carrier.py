# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_carrier.ui'
#
# Created: Mon Aug  6 16:00:25 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewCarrier(object):
    def setupUi(self, NewCarrier):
        NewCarrier.setObjectName("NewCarrier")
        NewCarrier.resize(400, 302)
        self.verticalLayout = QtGui.QVBoxLayout(NewCarrier)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(NewCarrier)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.codeLineEdit = QtGui.QLineEdit(NewCarrier)
        self.codeLineEdit.setObjectName("codeLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.codeLineEdit)
        self.label_2 = QtGui.QLabel(NewCarrier)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.nameLineEdit = QtGui.QLineEdit(NewCarrier)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nameLineEdit)
        self.label_3 = QtGui.QLabel(NewCarrier)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.rifLineEdit = QtGui.QLineEdit(NewCarrier)
        self.rifLineEdit.setObjectName("rifLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.rifLineEdit)
        self.label_4 = QtGui.QLabel(NewCarrier)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.emailLineEdit = QtGui.QLineEdit(NewCarrier)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.emailLineEdit)
        self.label_5 = QtGui.QLabel(NewCarrier)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.telLineEdit = QtGui.QLineEdit(NewCarrier)
        self.telLineEdit.setObjectName("telLineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.telLineEdit)
        self.label_6 = QtGui.QLabel(NewCarrier)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.addressLineEdit = QtGui.QLineEdit(NewCarrier)
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.addressLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.label_7 = QtGui.QLabel(NewCarrier)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(NewCarrier)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.createCarrierButton = QtGui.QPushButton(NewCarrier)
        self.createCarrierButton.setObjectName("createCarrierButton")
        self.horizontalLayout.addWidget(self.createCarrierButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewCarrier)
        QtCore.QMetaObject.connectSlotsByName(NewCarrier)

    def retranslateUi(self, NewCarrier):
        NewCarrier.setWindowTitle(QtGui.QApplication.translate("NewCarrier", "Nueva transportista", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewCarrier", "Código*", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewCarrier", "Nombre*", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewCarrier", "RIF", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewCarrier", "Corrreo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("NewCarrier", "Teléfono", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("NewCarrier", "Dirección", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("NewCarrier", "* Campos obligatorios", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("NewCarrier", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.createCarrierButton.setText(QtGui.QApplication.translate("NewCarrier", "Crear transportista", None, QtGui.QApplication.UnicodeUTF8))

