# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_add_truck import Ui_AddTruck
from mango.models.truck import Truck
from .add_carrier import AddCarrier
from .error_message_box import ErrorMessageBox
from .error_message_box import NewErrorMessageBox

class AddTruck(QtGui.QDialog):
  def __init__(self, parent):
    super(AddTruck, self).__init__(parent)
    self.ui = Ui_AddTruck()
    self.ui.setupUi(self)
    self.api = parent.api
    self.api.get_trucks()
    self.ui.frequentWidget.setEnabled(False)
    self.carrier = None

    self.trucksTableModel = TrucksTableModel([], self)
    self.filterTrucksProxyModel = QtGui.QSortFilterProxyModel()
    self.filterTrucksProxyModel.setSourceModel(self.trucksTableModel)
    self.filterTrucksProxyModel.setFilterKeyColumn(-1)
    self.filterTrucksProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.trucksTableView.setModel(self.filterTrucksProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterTrucksProxyModel.setFilterRegExp)

    self.api.getTrucksFinished.connect(self.trucksTableModel.refreshTrucks)
    self.api.createCarrierFinished.connect(self.setCarrier)
    self.api.createTruckFinished.connect(self.createTruckFinished)
    self.api.createTruckFailed.connect(self.createTruckFailed)
    self.ui.newButton.clicked.connect(self.enableTruckType)
    self.ui.frequentButton.clicked.connect(self.enableTruckType)
    self.ui.addCarrierButton.clicked.connect(self.addCarrier)
    self.ui.addButton.clicked.connect(self.addTruck)
    self.ui.trucksTableView.doubleClicked.connect(self.addTruck)
    self.ui.cancelButton.clicked.connect(self.reject)

  def addCarrier(self):
    addCarrierDialog = AddCarrier(self)
    if addCarrierDialog.exec_() == QtGui.QDialog.Accepted:
      if addCarrierDialog.new:
        self.api.create_carrier(addCarrierDialog.carrier)
      else:
        self.setCarrier(addCarrierDialog.carrier)

  def addTruck(self):
    if self.ui.newButton.isChecked():
      errors = []
      license_plate = self.ui.licensePlateLineEdit.text()
      carrier_id = self.carrier.id if self.carrier else None
      frequent = self.ui.saveAsFrequentBox.isChecked()
      truck = Truck(carrier_id, license_plate, frequent)

      self.api.create_truck(truck)
    else:
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

  def createTruckFinished(self, truck):
    self.truck = truck
    self.accept()

  def createTruckFailed(self, errors):
    NewErrorMessageBox(errors).exec_()

  def setCarrier(self, carrier):
    self.carrier = carrier
    self.ui.carrierLineEdit.setText(carrier.name)

  def enableTruckType(self):
    if self.ui.newButton.isChecked():
      self.ui.newWidget.setEnabled(True)
      self.ui.frequentWidget.setEnabled(False)
    else:
      self.ui.newWidget.setEnabled(False)
      self.ui.frequentWidget.setEnabled(True)


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
