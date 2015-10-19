# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_add_driver import Ui_AddDriver
from mango.models.driver import Driver
from .error_message_box import ErrorMessageBox
from .error_message_box import NewErrorMessageBox

class AddDriver(QtGui.QDialog):
  def __init__(self, parent):
    super(AddDriver, self).__init__(parent)
    self.ui = Ui_AddDriver()
    self.ui.setupUi(self)
    self.api = parent.api
    self.api.get_drivers()
    self.ui.frequentWidget.setEnabled(False)

    self.driversTableModel = DriversTableModel([], self)
    self.filterDriversProxyModel = QtGui.QSortFilterProxyModel()
    self.filterDriversProxyModel.setSourceModel(self.driversTableModel)
    self.filterDriversProxyModel.setFilterKeyColumn(-1)
    self.filterDriversProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.driversTableView.setModel(self.filterDriversProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterDriversProxyModel.setFilterRegExp)

    self.api.getDriversFinished.connect(self.driversTableModel.refreshDrivers)
    self.api.createDriverFinished.connect(self.createDriverFinished)
    self.api.createDriverFailed.connect(self.createDriverFailed)
    self.ui.newButton.clicked.connect(self.enableDriverType)
    self.ui.frequentButton.clicked.connect(self.enableDriverType)
    self.ui.addButton.clicked.connect(self.addDriver)
    self.ui.driversTableView.doubleClicked.connect(self.addDriver)
    self.ui.cancelButton.clicked.connect(self.reject)

  def addDriver(self):
    if self.ui.newButton.isChecked():
      name = self.ui.nameLineEdit.text()
      ci = self.ui.ciLineEdit.text()
      frequent = self.ui.saveAsFrequentBox.isChecked()
      driver = Driver(ci, name, frequent)

      self.api.create_driver(driver)
    else:
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

  def createDriverFinished(self, driver):
    self.driver = driver
    self.accept()

  def createDriverFailed(self, errors):
    NewErrorMessageBox(errors).exec_()

  def enableDriverType(self):
    if self.ui.newButton.isChecked():
      self.ui.newWidget.setEnabled(True)
      self.ui.frequentWidget.setEnabled(False)
    else:
      self.ui.newWidget.setEnabled(False)
      self.ui.frequentWidget.setEnabled(True)

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
