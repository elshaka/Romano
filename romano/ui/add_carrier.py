# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_add_carrier import Ui_AddCarrier
from mango.models.carrier import Carrier

from .error_message_box import ErrorMessageBox

class AddCarrier(QtGui.QDialog):
  def __init__(self, parent):
    super(AddCarrier, self).__init__(parent)
    self.api = parent.api
    self.ui = Ui_AddCarrier()
    self.ui.setupUi(self)
    self.api.get_carriers()
    self.ui.frequentWidget.setEnabled(False)

    self.carriersTableModel = CarriersTableModel([], self)
    self.filterCarriersProxyModel = QtGui.QSortFilterProxyModel()
    self.filterCarriersProxyModel.setSourceModel(self.carriersTableModel)
    self.filterCarriersProxyModel.setFilterKeyColumn(-1)
    self.filterCarriersProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.carriersTableView.setModel(self.filterCarriersProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterCarriersProxyModel.setFilterRegExp)

    self.api.getCarriersFinished.connect(self.carriersTableModel.refreshCarriers)
    self.ui.newButton.clicked.connect(self.enableCarrierType)
    self.ui.frequentButton.clicked.connect(self.enableCarrierType)
    self.ui.carriersTableView.doubleClicked.connect(self.addCarrier)
    self.ui.addButton.clicked.connect(self.addCarrier)
    self.ui.cancelButton.clicked.connect(self.reject)

  def addCarrier(self):
    if self.ui.newButton.isChecked():
      errors = []
      name = self.ui.nameLineEdit.text()
      if name == "":
        errors.append("Debe indicar un nombre")
      if not errors:
        self.new = True
        self.carrier = Carrier(name, None)
        if self.ui.saveAsFrequentBox.isChecked():
          self.carrier.frequent = True
        self.accept()
      else:
        ErrorMessageBox(errors).exec_()
    else:
      errors = []
      carrierFilteredIndex = self.ui.carriersTableView.currentIndex()
      if carrierFilteredIndex.row() == -1:
        errors.append("Debe seleccionar una transportista")
      if not errors:
        self.new = False
        carrierIndex = self.filterCarriersProxyModel.mapToSource(carrierFilteredIndex)
        self.carrier = self.carriersTableModel.getCarrier(carrierIndex.row())        
        self.accept()
      else:
        ErrorMessageBox(errors).exec_()

  def enableCarrierType(self):
    if self.ui.newButton.isChecked():
      self.ui.newWidget.setEnabled(True)
      self.ui.frequentWidget.setEnabled(False)
    else:
      self.ui.newWidget.setEnabled(False)
      self.ui.frequentWidget.setEnabled(True)

class CarriersTableModel(QtCore.QAbstractTableModel):
  def __init__(self, carriers, parent):
    super(CarriersTableModel, self).__init__(parent)
    self._carriers = carriers
    self._headers = ['Nombre']
    
  def getCarrier(self, row):
    return self._carriers[row]
    
  def refreshCarriers(self, carriers):
    self.beginResetModel()
    self._carriers = carriers
    self.endResetModel()

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]
        
  def rowCount(self, parent):
    return len(self._carriers)
    
  def columnCount(self, parent):
    return len(self._headers)
    
  def data(self, index, role):
    row = index.row()
    column = index.column()
    
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._carriers[row].name
