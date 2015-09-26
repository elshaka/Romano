# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_change_truck import Ui_ChangeTruck
from mango.models.truck import Truck
from .error_message_box import ErrorMessageBox

class ChangeTruck(QtGui.QDialog):
  def __init__(self, parent):
    super(ChangeTruck, self).__init__(parent)
    self.ui = Ui_ChangeTruck()
    self.ui.setupUi(self)
    self.api = parent.api
    self.api.get_trucks()

    self.trucksTableModel = TrucksTableModel([], self)
    self.filterTrucksProxyModel = QtGui.QSortFilterProxyModel()
    self.filterTrucksProxyModel.setSourceModel(self.trucksTableModel)
    self.filterTrucksProxyModel.setFilterKeyColumn(-1)
    self.filterTrucksProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.trucksTableView.setModel(self.filterTrucksProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterTrucksProxyModel.setFilterRegExp)

    self.api.getTrucksFinished.connect(self.trucksTableModel.refreshTrucks)
    self.ui.changeButton.clicked.connect(self.changeTruck)
    self.ui.trucksTableView.doubleClicked.connect(self.changeTruck)
    self.ui.cancelButton.clicked.connect(self.reject)

  def changeTruck(self):
    errors = []
    truckFilteredIndex = self.ui.trucksTableView.currentIndex()
    if truckFilteredIndex.row() == -1:
      errors.append("Debe seleccionar un camión")
    if not errors:
      self.new = False
      truckIndex = self.filterTrucksProxyModel.mapToSource(truckFilteredIndex)
      self.truck = self.trucksTableModel.getTruck(truckIndex.row())
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

class TrucksTableModel(QtCore.QAbstractTableModel):
  def __init__(self, trucks, parent):
    super(TrucksTableModel, self).__init__(parent)
    self._trucks = trucks
    self._headers = ['Placa', 'Transportista']

  def getTruck(self, row):
    return self._trucks[row]

  def refreshTrucks(self, trucks):
    self.beginResetModel()
    self._trucks = trucks
    self.endResetModel()

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]

  def rowCount(self, parent):
    return len(self._trucks)

  def columnCount(self, parent):
    return len(self._headers)

  def data(self, index, role):
    row = index.row()
    column = index.column()

    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._trucks[row].license_plate
      elif column == 1:
        return self._trucks[row].carrier.name
