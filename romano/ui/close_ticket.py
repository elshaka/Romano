# -*- coding: utf-8 -*-

import ConfigParser
from PySide import QtGui, QtCore
from ui_close_ticket import Ui_CloseTicket
from mango.models.ticket import Ticket
from serial_thread.serial_thread import SerialThread
from add_client import AddClient
from add_transaction import AddTransaction
from error_message_box import ErrorMessageBox

class CloseTicket(QtGui.QDialog):
  def __init__(self, ticket, allow_manual, parent):
    super(CloseTicket, self).__init__(parent)
    config = ConfigParser.ConfigParser()
    config.read('settings.ini')
    
    self.tolerance = int(config.get('Other','Tolerance'))
    self.api = parent.api
    self.ticket = ticket
    self.ui = Ui_CloseTicket()
    self.ui.setupUi(self)
    self.setModal(True)

    self.client = None

    if not allow_manual:
      self.ui.manualCheckBox.hide()

    self.ui.numberLineEdit.setText(str(ticket.number))
    self.ui.driverLineEdit.setText("%s - %s" % (ticket.driver.ci, ticket.driver.name))
    self.ui.truckLineEdit.setText("%s - %s" % (ticket.truck.license_plate, ticket.truck.carrier.name))
    self.ui.incomingWeightSpinBox.setValue(ticket.incoming_weight)
    self.ui.commentPlainTextEdit.setPlainText(ticket.comment)

    self.transactionsTableModel = TransactionsTableModel([], [], self)
    self.ui.transactionsTableView.setModel(self.transactionsTableModel)
    
    horizontalHeader = self.ui.transactionsTableView.horizontalHeader()
    horizontalHeader.setResizeMode(QtGui.QHeaderView.Stretch)
    
    if self.ticket.ticket_type_id == 1:
      self.ui.providerWidget.show()
      self.ui.receptionButton.setChecked(True)
    else:
      self.ui.providerWidget.hide()
      self.ui.dispatchButton.setChecked(True)

    self.ui.addClientButton.clicked.connect(self.addClient)
    self.ui.manualCheckBox.stateChanged.connect(self.setManualCapture)
    self.ui.outgoingWeightSpinBox.valueChanged.connect(self.weightChanged)
    self.ui.receptionButton.clicked.connect(self.updateTicketType)
    self.ui.dispatchButton.clicked.connect(self.updateTicketType)
    self.ui.addTransactionButton.clicked.connect(self.addTransaction)
    self.ui.cancelButton.clicked.connect(self.reject)
    self.ui.closeTicketButton.clicked.connect(self.closeTicket)
    self.ui.transactionsTableView.clicked.connect(self.enableDeleteTransaction)
    self.ui.removeTransactionButton.clicked.connect(self.removeTransaction)
    self.transactionsTableModel.totalChanged.connect(self.ui.transactionsTotalSpinBox.setValue)
      
    self.st = SerialThread(config.get('Serial','PortName'), config.get('Serial','Regex'), config.getboolean('Serial','Simulate'))
    self.st.dataReady.connect(self.getWeight, QtCore.Qt.QueuedConnection)
    self.st.start()
    
  def updateTicketType(self):
    weight = self.ui.outgoingWeightSpinBox.value()
    if self.ui.receptionButton.isChecked():
      self.ui.providerWidget.show()
      gross_weight = self.ticket.incoming_weight
      tare_weight = weight
    else:
      self.ui.providerWidget.hide()
      gross_weight = weight
      tare_weight = self.ticket.incoming_weight
    net_weight = gross_weight - tare_weight
    self.ui.grossWeightSpinBox.setValue(gross_weight)
    self.ui.tareWeightSpinBox.setValue(tare_weight)
    self.ui.netWeightSpinBox.setValue(net_weight)
    
  def addTransaction(self):
    if self.ticket.ticket_type_id == 1:
      transaction_type_id = 4
    else:
      transaction_type_id = 5
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

    if self.ui.receptionButton.isChecked():
      self.ticket.ticket_type_id = 1
    elif self.ui.dispatchButton.isChecked():
      self.ticket.ticket_type_id = 2

    errors = []
    if self.client == None:
      errors.append(u"Debe seleccionar un cliente/fábrica")
    if abs(net_weight - transactions_total) > self.tolerance:
      errors.append(u'La diferencia entre el peso neto y el total de transacciones es muy grande')
    if self.client == None:
      errors.append(u'El cliente/fábrica no ha sido seleccionado')
    if not weight_captured and not manualEnabled:
      errors.append('El peso de salida no ha sido capturado')
    if self.ticket.ticket_type_id == 1:
      if abs(provider_weight - net_weight) > self.tolerance:
        errors.append('La diferencia entre el peso neto y el peso del proveedor es muy grande')
      if provider_document_number == '':
        errors.append(u'El número de guía no ha sido indicado')
        
    if not errors:
      self.ticket.comment = self.ui.commentPlainTextEdit.toPlainText()
      self.ticket.outgoing_weight = outgoing_weight
      if self.ticket.ticket_type_id == 1:
        self.ticket.provider_weight = provider_weight
        self.ticket.provider_document_number = provider_document_number
      self.ticket.transactions_attributes = self.transactionsTableModel.getTransactions()
      
      for transaction in self.ticket.transactions_attributes:
        if self.ticket.ticket_type_id == 1:
          transaction.transaction_type_id = 4
        else:
          transaction.transaction_type_id = 5

      self.ticket.client_id = self.client.id
      self.ticket.manual_outgoing = manualEnabled

      self.accept()
    else:
      ErrorMessageBox(errors).exec_()
  
  def setManualCapture(self):
    if self.ui.manualCheckBox.isChecked():
      self.ui.outgoingWeightSpinBox.setEnabled(True)
      self.ui.captureWeightButton.setEnabled(False)
      self.ui.captureWeightButton.setChecked(False)
    else:
      self.ui.outgoingWeightSpinBox.setEnabled(False)
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
    self.client = client
    self.ui.clientLineEdit.setText(self.client.name)

class TransactionsTableModel(QtCore.QAbstractTableModel):
  totalChanged = QtCore.Signal(float)
  def __init__(self, transactions, lots, parent):
    super(TransactionsTableModel, self).__init__(parent)
    self._transactions = transactions
    self._lots = lots
    self._headers = [u'Lote', u'Código', 'Nombre', 'Sacos', 'Kg/Saco', 'Cantidad']
    
  def getTransactions(self):
    return self._transactions
  
  def addTransaction(self, transaction, lot):
    row = len(self._lots)
    self.beginInsertRows(QtCore.QModelIndex(), row, row)
    self._transactions.append(transaction)
    self._lots.append(lot)
    self.endInsertRows()
    self._recalculateTotal()
  
  def removeTransaction(self, row):
    self.beginResetModel()
    transaction = self._transactions[row]
    lot = self._lots[row]
    self._transactions.remove(transaction)
    self._lots.remove(lot)
    self.endResetModel()
    self._recalculateTotal()
    
  def _recalculateTotal(self):
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
