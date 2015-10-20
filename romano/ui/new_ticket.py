# -*- coding: utf-8 -*-

import os
import configparser
from PySide import QtGui, QtCore
from .ui_new_ticket import Ui_NewTicket
from mango.models.ticket import Ticket
from serial_thread.serial_thread import SerialThread
from .error_message_box import ErrorMessageBox
from .add_driver import AddDriver
from .add_truck import AddTruck

class NewTicket(QtGui.QDialog):
  def __init__(self, ticket_type_id, allow_manual, parent):
    super(NewTicket, self).__init__(parent)
    config = configparser.ConfigParser()
    settings_path = os.path.abspath(os.path.dirname(__file__))
    config.read(os.path.join(settings_path, 'settings.ini'))

    self.api = parent.api
    self.ticket_type_id = ticket_type_id
    self.ui = Ui_NewTicket()
    self.ui.setupUi(self)
    if ticket_type_id == 1:
      self.setWindowTitle("Nueva Recepción")
    else:
      self.setWindowTitle("Nuevo Despacho")
    self.setModal(True)

    self.driver = None
    self.truck = None

    if not allow_manual:
      self.ui.manualCheckBox.hide()

    self.api.createDriverFinished.connect(self.setDriver)
    self.api.createTruckFinished.connect(self.setTruck)
    self.ui.addDriverButton.clicked.connect(self.addDriver)
    self.ui.addTruckButton.clicked.connect(self.addTruck)
    self.ui.manualCheckBox.stateChanged.connect(self.setManualCapture)
    self.ui.createTicketButton.clicked.connect(self.createTicket)
    self.ui.cancelButton.clicked.connect(self.reject)

    self.st = SerialThread(
      config.get('Serial','PortName'),
      config.get('Serial','Regex'),
      config.getint('Serial', 'Baudrate'),
      config.get('Serial', 'Parity'),
      config.getint('Serial', 'Bytesize'),
      config.getboolean('Serial','Simulate')
    )
    self.st.dataReady.connect(self.getWeight, QtCore.Qt.QueuedConnection)
    self.st.start()

  def createTicket(self):
    weightCaptured = self.ui.captureWeightButton.isChecked()
    manualEnabled = self.ui.manualCheckBox.isChecked()

    errors = []
    if self.driver == None:
      errors.append("El chofer no ha sido seleccionado")
    if self.truck == None:
      errors.append("El camión no ha sido seleccionado")
    if not manualEnabled and not weightCaptured:
      errors.append("El peso de entrada no ha sido capturado")

    if not errors:
      incoming_weight = self.ui.incomingWeightSpinBox.value()
      comment = self.ui.commentPlainTextEdit.toPlainText()
      self.ticket = Ticket(self.ticket_type_id, self.driver.id, self.truck.id,
                           incoming_weight, comment)
      self.ticket.manual_incoming = manualEnabled
      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

  def addDriver(self):
    addDriverDialog = AddDriver(self)
    if addDriverDialog.exec_() == QtGui.QDialog.Accepted:
      self.setDriver(addDriverDialog.driver)

  def setDriver(self, driver):
    self.driver = driver
    self.ui.driverLineEdit.setText("%s - %s" % (self.driver.name, self.driver.ci))

  def addTruck(self):
    addTruckDialog = AddTruck(self)
    if addTruckDialog.exec_() == QtGui.QDialog.Accepted:
      self.setTruck(addTruckDialog.truck)

  def setTruck(self, truck):
    self.truck = truck
    self.ui.truckLineEdit.setText("%s - %s" % (self.truck.license_plate, self.truck.carrier.name))

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
      return "%s - %s" % (self._drivers[row].name, self._drivers[row].ci)

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
