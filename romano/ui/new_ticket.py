# -*- coding: utf-8 -*-

import settings
from PySide import QtGui, QtCore
from ui_new_ticket import Ui_NewTicket
from mango.models.ticket import Ticket
from serial.serial_thread import SerialThread
from error_message_box import ErrorMessageBox

class NewTicket(QtGui.QDialog):
  def __init__(self, ticket_type_id, parent):
    super(NewTicket, self).__init__(parent)
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
    
    self.ui.createTicketButton.clicked.connect(self.createTicket)
    self.ui.cancelButton.clicked.connect(self.reject)
    
    self.st = SerialThread(settings.PORTNAME, settings.SIMULATE_WEIGHT)
    self.st.dataReady.connect(self.getWeight, QtCore.Qt.QueuedConnection)
    self.st.start()
        
  def createTicket(self):
    driverIndex = self.ui.driversComboBox.currentIndex()
    truckIndex = self.ui.trucksComboBox.currentIndex()
    weightCaptured = self.ui.captureWeightButton.isChecked()
    
    errors = []
    if driverIndex == -1:
      errors.append("El chofer no ha sido seleccionado")
    if truckIndex == -1:
      errors.append(u"El camión no ha sido seleccionado")
    if not weightCaptured:
      errors.append("El peso de entrada no ha sido capturado")
    
    if not errors:
      driver = self.ui.driversComboBox.model().getDriver(driverIndex)
      truck = self.ui.trucksComboBox.model().getTruck(truckIndex)
      incoming_weight = self.ui.incomingWeightSpinBox.value()
      comment = self.ui.commentTextEdit.toPlainText()
      self.ticket = Ticket(self.ticket_type_id, driver.id, truck.id, 
                           incoming_weight, comment)
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()
      
  def getWeight(self, weight):
    if not self.ui.captureWeightButton.isChecked():
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
