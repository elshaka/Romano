# -*- coding: utf-8 -*-

import os
import configparser
import pickle
from PySide import QtGui, QtCore
from .ui_close_ticket import Ui_CloseTicket
from mango.models.ticket import Ticket
from serial_thread.serial_thread import SerialThread
from .change_driver import ChangeDriver
from .change_truck import ChangeTruck
from .add_client import AddClient
from .add_transaction import AddTransaction
from .error_message_box import ErrorMessageBox

class CloseTicket(QtGui.QDialog):
  def __init__(self, ticket_data, allow_manual, parent):
    super(CloseTicket, self).__init__(parent)
    config = configparser.ConfigParser()
    settings_path = os.path.abspath(os.path.dirname(__file__))
    config.read(os.path.join(settings_path, 'settings.ini'))

    self.tolerance = config.getint('Other', 'Tolerance')
    self.api = parent.api

    self.ticket = ticket_data['ticket']
    self.previous_incoming_weight = self.ticket.incoming_weight
    self.allow_manual = allow_manual
    self.ui = Ui_CloseTicket()
    self.ui.setupUi(self)
    self.setModal(True)

    if hasattr(self.ticket, 'client'):
      self.setClient(self.ticket.client)

    if ticket_data['weight_captured']:
      self.ui.captureWeightButton.setChecked(True)
      self.ui.outgoingWeightSpinBox.setValue(self.ticket.outgoing_weight)

    self.old_driver = self.ticket.driver
    self.old_truck = self.ticket.truck

    self.reception_diff = self.dispatch_diff = self.max_diff = 0.5
    self.diff_ok = False
    self.transactions_diff_ok = False
    self.transactions_diff = 999

    self.api.getSettingsFinished.connect(self.updateSettings)
    self.api.get_settings()

    self.api.getFeaturesFinished.connect(self.updateFeatures)
    self.api.get_features()

    self.api.getDocumentTypesFinished.connect(self.updateDocumentTypes)
    self.api.get_document_types()

    if not self.allow_manual:
      self.ui.manualCheckBox.hide()

    self.ui.addressWidget.hide()
    self.ui.documentTypeWidget.hide()
    self.ui.numberLineEdit.setText(str(self.ticket.number))
    self.ui.driverLineEdit.setText("%s - %s" % (self.ticket.driver.ci, self.ticket.driver.name))
    self.ui.truckLineEdit.setText("%s - %s" % (self.ticket.truck.license_plate, self.ticket.truck.carrier.name))
    self.ui.incomingWeightSpinBox.setValue(self.ticket.incoming_weight)
    self.ui.commentPlainTextEdit.setPlainText(self.ticket.comment)

    self.transactionsTableModel = TransactionsTableModel(self.ticket.transactions_attributes, ticket_data['lots'], self)
    self.ui.transactionsTableView.setModel(self.transactionsTableModel)

    horizontalHeader = self.ui.transactionsTableView.horizontalHeader()
    horizontalHeader.resizeSection(0, 80)
    horizontalHeader.resizeSection(1, 80)
    horizontalHeader.setResizeMode(2, QtGui.QHeaderView.Stretch)
    horizontalHeader.resizeSection(3, 50)
    horizontalHeader.resizeSection(4, 50)
    horizontalHeader.resizeSection(5, 80)

    if self.ticket.ticket_type_id == 1:
      self.ui.receptionButton.setChecked(True)
    else:
      self.ui.dispatchButton.setChecked(True)

    self.ui.changeDriverButton.clicked.connect(self.changeDriver)
    self.ui.changeTruckButton.clicked.connect(self.changeTruck)
    self.ui.addClientButton.clicked.connect(self.addClient)
    self.ui.manualCheckBox.stateChanged.connect(self.setManualCapture)
    self.ui.outgoingWeightSpinBox.valueChanged.connect(self.weightChanged)
    self.ui.incomingWeightSpinBox.valueChanged.connect(self.updateTicketType)
    self.ui.netWeightSpinBox.valueChanged.connect(self.updateDiff)
    self.ui.providerWeightSpinBox.valueChanged.connect(self.updateDiff)
    self.ui.diffSpinBox.valueChanged.connect(self.updateDiffStyle)
    self.ui.receptionButton.clicked.connect(self.updateTicketType)
    self.ui.dispatchButton.clicked.connect(self.updateTicketType)
    self.ui.addTransactionButton.clicked.connect(self.addTransaction)
    self.ui.cancelButton.clicked.connect(self.cancel)
    self.ui.saveButton.clicked.connect(self.saveTicket)
    self.ui.closeTicketButton.clicked.connect(self.closeTicket)
    self.ui.transactionsTableView.clicked.connect(self.enableDeleteTransaction)
    self.ui.removeTransactionButton.clicked.connect(self.removeTransaction)
    self.transactionsTableModel.totalChanged.connect(self.updateTotal)
    self.transactionsTableModel.recalculateTotal()
    self.updateTicketType()

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

  def cancel(self):
    self.ticket.driver = self.old_driver
    self.reject()

  def updateTotal(self, total):
    self.ui.transactionsTotalSpinBox.setValue(total)
    if self.ui.dispatchButton.isChecked():
      self.ui.providerWeightSpinBox.setValue(self.ui.transactionsTotalSpinBox.value())
    self.updateDiff()

  def updateDiff(self):
    net_weight = self.ui.netWeightSpinBox.value()
    total = self.ui.providerWeightSpinBox.value()
    transactions_total = self.ui.transactionsTotalSpinBox.value()
    if total == 0:
      diff = 999
    else:
      diff = (net_weight - total) / total * 100
    if transactions_total == 0:
      self.transactions_diff = 999
    else:
      self.transactions_diff = (net_weight - transactions_total) / transactions_total * 100
    self.ui.diffSpinBox.setValue(diff)
    self.updateDiffStyle()

  def updateDiffStyle(self):
    diff = self.ui.diffSpinBox.value()
    if self.ui.receptionButton.isChecked():
      self.max_diff = self.reception_diff
    else:
      self.max_diff = self.dispatch_diff

    if diff >= -1 * self.max_diff and diff <= self.max_diff:
      bkg_color = "0, 0, 0"
      self.diff_ok = True
    else:
      bkg_color = "255, 0, 0"
      self.diff_ok = False

    self.transactions_diff_ok = self.transactions_diff >= -1 * self.max_diff and self.transactions_diff <= self.max_diff
    self.ui.diffSpinBox.setStyleSheet("background-color: rgb(%s);\ncolor: rgb(0, 170, 0);" % bkg_color)

  def updateSettings(self, settings):
    self.reception_diff = settings.ticket_reception_diff
    self.dispatch_diff = settings.ticket_dispatch_diff

  def updateFeatures(self, features):
    self.features = features
    if "multiple_addresses" in features:
      self.ui.addressWidget.show()
    if "document_types" in features:
      self.ui.documentTypeWidget.show()

  def updateDocumentTypes(self, document_types):
    self.documentTypeListModel = DocumentTypeListModel(document_types, self)
    self.ui.documentTypeComboBox.setModel(self.documentTypeListModel)

    try:
      row = self.documentTypeListModel.findRowById(self.ticket.document_type_id)
      self.ui.documentTypeComboBox.setCurrentIndex(row)
    except AttributeError:
      pass

  def updateTicketType(self):
    self.ticket.incoming_weight = self.ui.incomingWeightSpinBox.value()
    weight = self.ui.outgoingWeightSpinBox.value()
    if self.ui.receptionButton.isChecked():
      self.ui.providerWidget.show()
      gross_weight = self.ticket.incoming_weight
      tare_weight = weight
      self.ui.providerWeightSpinBox.setReadOnly(False)
    else:
      gross_weight = weight
      tare_weight = self.ticket.incoming_weight
      self.ui.providerWeightSpinBox.setReadOnly(True)
      self.ui.providerWeightSpinBox.setValue(self.ui.transactionsTotalSpinBox.value())

    net_weight = gross_weight - tare_weight
    self.ui.grossWeightSpinBox.setValue(gross_weight)
    self.ui.tareWeightSpinBox.setValue(tare_weight)
    self.ui.netWeightSpinBox.setValue(net_weight)

  def addTransaction(self):
    # TODO ELIMINAR
    if self.ticket.ticket_type_id == 1:
      transaction_type_id = 4
    else:
      transaction_type_id = 5
    # FIN TODO
    self.api.get_lots()
    self.api.get_product_lots()
    addTransactionDialog = AddTransaction(transaction_type_id, self)
    self.api.getLotsFinished.connect(addTransactionDialog.getLotsFinished)
    self.api.getProductLotsFinished.connect(addTransactionDialog.getProductLotsFinished)
    if addTransactionDialog.exec_() == QtGui.QDialog.Accepted:
      transaction = addTransactionDialog.transaction
      lot = addTransactionDialog.lot
      self.transactionsTableModel.addTransaction(transaction, lot)

  def removeTransaction(self):
    row = self.ui.transactionsTableView.currentIndex().row()
    self.transactionsTableModel.removeTransaction(row)
    currentRow = self.ui.transactionsTableView.currentIndex().row()
    if currentRow == -1:
      self.ui.removeTransactionButton.setEnabled(False)

  def enableDeleteTransaction(self, index):
    if index.row() != -1:
      self.ui.removeTransactionButton.setEnabled(True)

  def closeTicket(self):
    outgoing_weight = self.ui.outgoingWeightSpinBox.value()
    weight_captured = self.ui.captureWeightButton.isChecked()
    manualEnabled = self.ui.manualCheckBox.isChecked()
    net_weight = self.ui.netWeightSpinBox.value()
    provider_weight = self.ui.providerWeightSpinBox.value()
    provider_document_number = self.ui.providerDocumentNumberLineEdit.text()
    transactions_total = self.ui.transactionsTotalSpinBox.value()
    diff = self.ui.diffSpinBox.value()

    if self.ui.receptionButton.isChecked():
      self.ticket.ticket_type_id = 1
    elif self.ui.dispatchButton.isChecked():
      self.ticket.ticket_type_id = 2

    errors = []

    if not (self.diff_ok and self.transactions_diff_ok):
      if not self.allow_manual:
        if not self.diff_ok:
          errors.append('La diferencia entre el peso neto y peso proveedor es muy grande')
        if not self.transactions_diff_ok:
          errors.append('La diferencia entre el peso neto y el total de transacciones es muy grande')
      else:
        flags = QtGui.QMessageBox.StandardButton.Yes
        flags |= QtGui.QMessageBox.StandardButton.No
        diff_fields = []
        if not self.diff_ok:
          diff_fields.append("peso proveedor")
        if not self.transactions_diff_ok:
          diff_fields.append("transacciones")
        question = "¿Esta seguro de permitir una diferencia mayor a %s %% (%s)?" % (self.max_diff, ", ".join(diff_fields))
        response = QtGui.QMessageBox.question(self, "Advertencia", question, flags)
        if response == QtGui.QMessageBox.Yes:
          pass
        else:
          if not self.diff_ok:
            errors.append('La diferencia entre el peso neto y peso proveedor es muy grande')
          if not self.transactions_diff_ok:
            errors.append('La diferencia entre el peso neto y el total de transacciones es muy grande')

    if net_weight < 0:
      errors.append('El peso neto no puede ser negativo')
    if transactions_total == 0:
      errors.append('El total de transacciones no puede ser 0')
    if self.client == None:
      errors.append('El cliente/fábrica no ha sido seleccionado')
    elif "multiple_addresses" in self.features:
      self.ticket.address = self.ui.addressComboBox.currentText()
    else:
      self.ticket.address = self.client.address
    if not weight_captured and not manualEnabled:
      errors.append('El peso de salida no ha sido capturado')
    if provider_document_number == '':
      errors.append('El número de documento no ha sido indicado')

    if not errors:
      if "document_types" in self.features:
        index = self.ui.documentTypeComboBox.currentIndex()
        if index != -1:
          dt = self.documentTypeListModel.getDocumentType(index)
          self.ticket.document_type_id = dt.id
      self.ticket.comment = self.ui.commentPlainTextEdit.toPlainText()
      self.ticket.outgoing_weight = outgoing_weight

      self.ticket.provider_weight = provider_weight
      self.ticket.provider_document_number = provider_document_number
      self.ticket.transactions_attributes = self.transactionsTableModel.getTransactions()

      for transaction in self.ticket.transactions_attributes:
        if self.ticket.ticket_type_id == 1:
          transaction.transaction_type_id = 4
        else:
          transaction.transaction_type_id = 5
        delattr(transaction, 'content_comment')

      self.ticket.client_id = self.client.id
      self.ticket.driver_id = self.ticket.driver.id
      self.ticket.truck_id = self.ticket.truck.id
      self.ticket.manual_outgoing = manualEnabled
      self.ticket.manual_incoming |= self.previous_incoming_weight != self.ticket.incoming_weight

      self.accept()
    else:
      ErrorMessageBox(errors).exec_()

  def setManualCapture(self):
    if self.ui.manualCheckBox.isChecked():
      self.ui.outgoingWeightSpinBox.setEnabled(True)
      self.ui.incomingWeightSpinBox.setEnabled(True)
      self.ui.captureWeightButton.setEnabled(False)
      self.ui.captureWeightButton.setChecked(False)
    else:
      self.ui.outgoingWeightSpinBox.setEnabled(False)
      self.ui.incomingWeightSpinBox.setEnabled(False)
      self.ui.captureWeightButton.setEnabled(True)

  def getWeight(self, weight):
    if not self.ui.captureWeightButton.isChecked() and not self.ui.manualCheckBox.isChecked():
      self.ui.outgoingWeightSpinBox.setValue(weight)

  def weightChanged(self, weight):
    if self.ui.dispatchButton.isChecked():
      gross_weight = weight
      tare_weight = self.ticket.incoming_weight
    else:
      gross_weight = self.ticket.incoming_weight
      tare_weight = weight
    net_weight = gross_weight - tare_weight
    self.ui.grossWeightSpinBox.setValue(gross_weight)
    self.ui.tareWeightSpinBox.setValue(tare_weight)
    self.ui.netWeightSpinBox.setValue(net_weight)

  def addClient(self):
    addClientDialog = AddClient(self)
    if addClientDialog.exec_() == QtGui.QDialog.Accepted:
      self.setClient(addClientDialog.client)

  def setClient(self, client):
    try:
      self.client = client
      self.ui.clientLineEdit.setText(self.client.name)
      self.ui.addressComboBox.clear()
      self.ui.addressComboBox.addItem(client.address)
      self.ui.addressComboBox.addItems(client.addresses)

      self.ui.addressComboBox.setCurrentIndex(self.ui.addressComboBox.findText(self.ticket.address))
    except AttributeError:
      pass

  def changeDriver(self):
    changeDriverDialog = ChangeDriver(self)
    if changeDriverDialog.exec_() == QtGui.QDialog.Accepted:
      self.setDriver(changeDriverDialog.driver)

  def setDriver(self, driver):
    self.ticket.driver = driver
    self.ui.driverLineEdit.setText("%s - %s" % (self.ticket.driver.ci, self.ticket.driver.name))

  def changeTruck(self):
    changeTruckDialog = ChangeTruck(self)
    if changeTruckDialog.exec_() == QtGui.QDialog.Accepted:
      self.setTruck(changeTruckDialog.truck)

  def setTruck(self, truck):
    self.ticket.truck = truck
    self.ui.truckLineEdit.setText("%s - %s" % (self.ticket.truck.license_plate, self.ticket.truck.carrier.name))

  def saveTicket(self):
    self.ticket.ticket_type_id = 1 if self.ui.receptionButton.isChecked() else 2

    if "multiple_addresses" in self.features:
      self.ticket.address = self.ui.addressComboBox.currentText()
    elif self.client:
      self.ticket.address = self.client.address

    if "document_types" in self.features:
      index = self.ui.documentTypeComboBox.currentIndex()
      if index != -1:
        dt = self.documentTypeListModel.getDocumentType(index)
        self.ticket.document_type_id = dt.id

    self.ticket.comment = self.ui.commentPlainTextEdit.toPlainText()

    self.ticket.outgoing_weight = self.ui.outgoingWeightSpinBox.value()
    self.ticket.provider_weight = self.ui.providerWeightSpinBox.value()
    self.ticket.provider_document_number = self.ui.providerDocumentNumberLineEdit.text()
    self.ticket.transactions_attributes = self.transactionsTableModel.getTransactions()

    self.ticket.client = self.client

    self.ticket.manual_outgoing = self.ui.manualCheckBox.isChecked()
    self.ticket.manual_incoming |= self.previous_incoming_weight != self.ticket.incoming_weight

    ticket_data = {
      'ticket': self.ticket,
      'weight_captured': self.ui.captureWeightButton.isChecked(),
      'lots': self.transactionsTableModel.getLots()
    }

    fileObject = open("%s.ticket" % self.ticket.number, 'wb')
    pickle.dump(ticket_data, fileObject)
    fileObject.close()

    print("Se guardó el ticket %s" % self.ticket.number)

    self.reject()

class TransactionsTableModel(QtCore.QAbstractTableModel):
  totalChanged = QtCore.Signal(float)
  def __init__(self, transactions, lots, parent):
    super(TransactionsTableModel, self).__init__(parent)
    self._transactions = transactions
    self._lots = lots
    self._headers = ['Lote', 'Código', 'Nombre', 'Sacos', 'Kg/Saco', 'Cantidad']
    self.recalculateTotal()

  def getTransactions(self):
    return self._transactions

  def getLots(self):
    return self._lots

  def addTransaction(self, transaction, lot):
    row = len(self._lots)
    self.beginInsertRows(QtCore.QModelIndex(), row, row)
    self._transactions.append(transaction)
    self._lots.append(lot)
    self.endInsertRows()
    self.recalculateTotal()

  def removeTransaction(self, row):
    self.beginResetModel()
    transaction = self._transactions[row]
    lot = self._lots[row]
    self._transactions.remove(transaction)
    self._lots.remove(lot)
    self.endResetModel()
    self.recalculateTotal()

  def recalculateTotal(self):
    total = 0.0
    for t in self._transactions:
      total += t.amount
    self.totalChanged.emit(total)

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]

  def rowCount(self, parent):
    return len(self._lots)

  def columnCount(self, parent):
    return len(self._headers)

  def data(self, index, role):
    row = index.row()
    column = index.column()
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._lots[row].code
      elif column == 1:
        return self._lots[row].content_code
      elif column == 2:
        return self._lots[row].content_name
      elif column == 3:
        if self._transactions[row].sack:
          return self._transactions[row].sacks
        else:
          return "-"
      elif column == 4:
        if self._transactions[row].sack:
          return self._transactions[row].sack_weight
        else:
          return "-"
      elif column == 5:
        return "%s Kg" % self._transactions[row].amount
    elif role == QtCore.Qt.TextAlignmentRole:
      if column == 5:
        return QtCore.Qt.AlignRight
      else:
        return QtCore.Qt.AlignLeft
    elif role == QtCore.Qt.ToolTipRole:
      comment = self._transactions[row].content_comment
      if comment:
        return self._transactions[row].content_comment
      else:
        return ""

class DocumentTypeListModel(QtCore.QAbstractListModel):
  def __init__(self, document_types, parent):
    super(DocumentTypeListModel, self).__init__(parent)
    self._document_types = document_types

  def rowCount(self, parent):
    return len(self._document_types)

  def data(self, index, role):
    row = index.row()
    column = index.column()
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._document_types[row].name

  def refreshDocumentTypes(self, document_types):
    self.beginResetModel()
    self._document_types = document_types
    self.endResetModel()

  def getDocumentType(self, row):
    return self._document_types[row]

  def findRowById(self, document_type_id):
    row = -1
    for index, dt in enumerate(self._document_types):
      if dt.id == document_type_id:
        row = index
        break
    return row
