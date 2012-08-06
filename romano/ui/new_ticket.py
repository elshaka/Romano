# -*- coding: utf-8 -*-

import settings
from PySide import QtGui, QtCore
from ui_new_ticket import Ui_NewTicket
from mango.models.ticket import Ticket
from serial_thread.serial_thread import SerialThread
from error_message_box import ErrorMessageBox
from new_driver import NewDriver
from new_truck import NewTruck

class NewTicket(QtGui.QDialog):
  def __init__(self, ticket_type_id, allow_manual, parent):
    super(NewTicket, self).__init__(parent)
    self.api = parent.api
    self.ticket_type_id = ticket_type_id    
    self.ui = Ui_NewTicket()
    self.ui.setupUi(self)
    if ticket_type_id == 1:
      self.setWindowTitle(u"Nueva Recepción")
    else:
      self.setWindowTitle(u"Nuevo Despacho")
    self.setModal(True)
    driverLineEdit = self.ui.driversComboBox.lineEdit()
    driverLineEdit.setPlaceholderText(u"Buscar por cédula")
    driverCompleter = self.ui.driversComboBox.completer()
    driverCompleter.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    truckLineEdit = self.ui.trucksComboBox.lineEdit()
    truckLineEdit.setPlaceholderText("Buscar por placa")
    trucksCompleter = self.ui.trucksComboBox.completer()
    trucksCompleter.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    if not allow_manual:
      self.ui.manualCheckBox.hide()
    
    self.api.get_drivers()
    self.api.get_trucks()
    
    self.api.createDriverFinished.connect(self.refreshDrivers)
    self.api.createTruckFinished.connect(self.refreshTrucks)
    self.api.getDriversFinished.connect(self.getDriversFinished)
    self.api.getTrucksFinished.connect(self.getTrucksFinished)
    self.ui.addDriverButton.clicked.connect(self.newDriver)
    self.ui.addTruckButton.clicked.connect(self.newTruck)
    self.ui.manualCheckBox.stateChanged.connect(self.setManualCapture)
    self.ui.createTicketButton.clicked.connect(self.createTicket)
    self.ui.cancelButton.clicked.connect(self.reject)
    
    self.st = SerialThread(settings.PORTNAME, settings.SIMULATE_WEIGHT)
    self.st.dataReady.connect(self.getWeight, QtCore.Qt.QueuedConnection)
    self.st.start()
        
  def createTicket(self):
    driverIndex = self.ui.driversComboBox.currentIndex()
    truckIndex = self.ui.trucksComboBox.currentIndex()
    weightCaptured = self.ui.captureWeightButton.isChecked()
    manualEnabled = self.ui.manualCheckBox.isChecked()
    
    errors = []
    if driverIndex == -1:
      errors.append("El chofer no ha sido seleccionado")
    if truckIndex == -1:
      errors.append(u"El camión no ha sido seleccionado")
    if not manualEnabled and not weightCaptured:
      errors.append("El peso de entrada no ha sido capturado")
    
    if not errors:
      driver = self.ui.driversComboBox.model().getDriver(driverIndex)
      truck = self.ui.trucksComboBox.model().getTruck(truckIndex)
      incoming_weight = self.ui.incomingWeightSpinBox.value()
      comment = self.ui.commentPlainTextEdit.toPlainText()
      self.ticket = Ticket(self.ticket_type_id, driver.id, truck.id, 
                           incoming_weight, comment)
      self.ticket.manual_incoming = manualEnabled
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()
  
  def newDriver(self):
    newDriverDialog = NewDriver(self)
    if newDriverDialog.exec_() == QtGui.QDialog.Accepted:
      self.api.create_driver(newDriverDialog.driver)
      
  def refreshDrivers(self):
    self.api.get_drivers()
  
  def newTruck(self):
    newTruckDialog = NewTruck(self)
    if newTruckDialog.exec_() == QtGui.QDialog.Accepted:
      self.api.create_truck(newTruckDialog.truck)
    
  def refreshTrucks(self):
    self.api.get_trucks()
  
  def setManualCapture(self):
    if self.ui.manualCheckBox.isChecked():
      self.ui.incomingWeightSpinBox.setEnabled(True)
      self.ui.captureWeightButton.setEnabled(False)
      self.ui.captureWeightButton.setChecked(False)
    else:
      self.ui.incomingWeightSpinBox.setEnabled(False)
      self.ui.captureWeightButton.setEnabled(True)

  def getWeight(self, weight):
    if not self.ui.captureWeightButton.isChecked() and not self.ui.manualCheckBox.isChecked():
      self.ui.incomingWeightSpinBox.setValue(weight)
  
  def getDriversFinished(self, drivers):
    self.driversListModel = DriversListModel(drivers, self)
    self.ui.driversComboBox.setModel(self.driversListModel)
    self.ui.driversComboBox.setCurrentIndex(-1)

  def getTrucksFinished(self, trucks):
    self.trucksListModel = TrucksListModel(trucks, self)
    self.ui.trucksComboBox.setModel(self.trucksListModel)
    self.ui.trucksComboBox.setCurrentIndex(-1)
    
class DriversListModel(QtCore.QAbstractListModel):
  def __init__(self, drivers, parent):
    super(DriversListModel, self).__init__(parent)
    self._drivers = drivers

  def refreshDrivers(self, drivers):
    self.beginResetModel()
    self._drivers = drivers
    self.endResetModel()
    
  def getDriver(self, row):
    return self._drivers[row]
      
  def rowCount(self, parent):
    return len(self._drivers)
    
  def data(self, index, role):
    row = index.row()
    if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
      return "%s - %s" % (self._drivers[row].ci, self._drivers[row].name)

class TrucksListModel(QtCore.QAbstractListModel):
  def __init__(self, trucks, parent):
    super(TrucksListModel, self).__init__(parent)
    self._trucks = trucks

  def refreshTrucks(self, trucks):
    self.beginResetModel()
    self._trucks = trucks
    self.endResetModel()
    
  def getTruck(self, row):
    return self._trucks[row]
    
  def rowCount(self, parent):
    return len(self._trucks)
    
  def data(self, index, role):
    row = index.row()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
      return "%s - %s" % (self._trucks[row].license_plate, self._trucks[row].carrier.name)
