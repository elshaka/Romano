# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from ui_new_truck import Ui_NewTruck
from mango.models.truck import Truck
from new_carrier import NewCarrier

class NewTruck(QtGui.QDialog):
  def __init__(self, parent):
    super(NewTruck, self).__init__(parent)
    self.api = parent.api
    self.ui = Ui_NewTruck()
    self.ui.setupUi(self)

    self.api.get_carriers()
    
    carrierCompleter = self.ui.carriersComboBox.completer()
    carrierCompleter.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    self.api.createCarrierFinished.connect(self.refreshCarriers)
    self.api.getCarriersFinished.connect(self.getCarriersFinished)
    self.ui.addCarrierButton.clicked.connect(self.newCarrier)
    self.ui.createTruckButton.clicked.connect(self.createTruck)
    self.ui.cancelButton.clicked.connect(self.reject)
    
  def createTruck(self):
    license_plate = self.ui.licensePlateLineEdit.text()
    carrierIndex = self.ui.carriersComboBox.currentIndex()
    if carrierIndex != -1:
      license_plate = self.ui.licensePlateLineEdit.text()
      carrier = self.ui.carriersComboBox.model().getCarrier(carrierIndex)
      self.truck = Truck(carrier.id, license_plate)
      self.accept()
      
  def getCarriersFinished(self, carriers):
    self.carriersListModel = CarriersListModel(carriers, self)
    self.ui.carriersComboBox.setModel(self.carriersListModel)
    self.ui.carriersComboBox.setCurrentIndex(-1)

  def newCarrier(self):
    newCarrierDialog = NewCarrier(self)
    if newCarrierDialog.exec_() == QtGui.QDialog.Accepted:
      self.api.create_carrier(newCarrierDialog.carrier)
      
  def refreshCarriers(self):
    self.api.get_carriers()

class CarriersListModel(QtCore.QAbstractListModel):
  def __init__(self, carriers, parent):
    super(CarriersListModel, self).__init__(parent)
    self._carriers = carriers

  def refreshCarriers(self, carriers):
    self.beginResetModel()
    self._carriers = carriers
    self.endResetModel()
    
  def getCarrier(self, row):
    return self._carriers[row]
    
  def rowCount(self, parent):
    return len(self._carriers)
    
  def data(self, index, role):
    row = index.row()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
      return self._carriers[row].name
