# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_change_driver import Ui_ChangeDriver
from mango.models.driver import Driver
from .error_message_box import ErrorMessageBox

class ChangeDriver(QtGui.QDialog):
  def __init__(self, parent):
    super(ChangeDriver, self).__init__(parent)
    self.ui = Ui_ChangeDriver()
    self.ui.setupUi(self)
    self.api = parent.api
    self.api.get_drivers()

    self.driversTableModel = DriversTableModel([], self)
    self.filterDriversProxyModel = QtGui.QSortFilterProxyModel()
    self.filterDriversProxyModel.setSourceModel(self.driversTableModel)
    self.filterDriversProxyModel.setFilterKeyColumn(-1)
    self.filterDriversProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.driversTableView.setModel(self.filterDriversProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterDriversProxyModel.setFilterRegExp)

    self.api.getDriversFinished.connect(self.driversTableModel.refreshDrivers)
    self.ui.changeButton.clicked.connect(self.changeDriver)
    self.ui.driversTableView.doubleClicked.connect(self.changeDriver)
    self.ui.cancelButton.clicked.connect(self.reject)

  def changeDriver(self):
    errors = []
    driverFilteredIndex = self.ui.driversTableView.currentIndex()
    if driverFilteredIndex.row() == -1:
      errors.append("Debe seleccionar un chofer")
    if not errors:
      driverIndex = self.filterDriversProxyModel.mapToSource(driverFilteredIndex)
      self.driver = self.driversTableModel.getDriver(driverIndex.row())
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

class DriversTableModel(QtCore.QAbstractTableModel):
  def __init__(self, drivers, parent):
    super(DriversTableModel, self).__init__(parent)
    self._drivers = drivers
    self._headers = ['Cédula', 'Nombre']

  def getDriver(self, row):
    return self._drivers[row]

  def refreshDrivers(self, drivers):
    self.beginResetModel()
    self._drivers = drivers
    self.endResetModel()

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]

  def rowCount(self, parent):
    return len(self._drivers)

  def columnCount(self, parent):
    return len(self._headers)

  def data(self, index, role):
    row = index.row()
    column = index.column()

    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._drivers[row].ci
      elif column == 1:
        return self._drivers[row].name
