# -*- coding: utf-8 -*-

import settings
from PySide import QtGui, QtCore
from ui_close_ticket import Ui_CloseTicket
from mango.models.ticket import Ticket
from serial_thread.serial_thread import SerialThread
from add_transaction import AddTransaction
from error_message_box import ErrorMessageBox

class CloseTicket(QtGui.QDialog):
  def __init__(self, ticket, allow_manual, parent):
    super(CloseTicket, self).__init__(parent)
    self.tolerance = settings.TOLERANCE
    self.api = parent.api
    self.ticket = ticket
    self.ui = Ui_CloseTicket()
    self.ui.setupUi(self)
    self.setModal(True)
    clientsCompleter = self.ui.clientsComboBox.completer()
    clientsCompleter.setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    if not allow_manual:
      self.ui.manualCheckBox.hide()
    
    self.ui.numberLineEdit.setText(str(ticket.number))
    self.ui.ticketTypeLineEdit.setText(ticket.ticket_type.code)
    self.ui.driverLineEdit.setText("%s - %s" % (ticket.driver.ci, ticket.driver.name))
    self.ui.truckLineEdit.setText("%s - %s" % (ticket.truck.license_plate, ticket.truck.carrier.name))
    self.ui.incomingWeightSpinBox.setValue(ticket.incoming_weight)
    self.ui.commentPlainTextEdit.setPlainText(ticket.comment)
    
    self.transactionsTableModel = TransactionsTableModel([], [], self)
    self.ui.transactionsTableView.setModel(self.transactionsTableModel)
    
    horizontalHeader = self.ui.transactionsTableView.horizontalHeader()
    horizontalHeader.setResizeMode(QtGui.QHeaderView.Stretch)
    
    if self.ticket.ticket_type_id != 1:
      self.ui.providerWidget.hide()
    
    self.ui.manualCheckBox.stateChanged.connect(self.setManualCapture)
    self.ui.outgoingWeightSpinBox.valueChanged.connect(self.weightChanged)
    self.ui.clientButton.clicked.connect(self.showClients)
    self.ui.factoryButton.clicked.connect(self.showFactories)
    self.ui.addTransactionButton.clicked.connect(self.addTransaction)
    self.ui.cancelButton.clicked.connect(self.reject)
    self.ui.closeTicketButton.clicked.connect(self.closeTicket)
    self.ui.transactionsTableView.clicked.connect(self.enableDeleteTransaction)
    self.ui.removeTransactionButton.clicked.connect(self.removeTransaction)
    self.transactionsTableModel.totalChanged.connect(self.ui.transactionsTotalSpinBox.setValue)
      
    self.st = SerialThread(settings.PORTNAME, settings.SIMULATE_WEIGHT)
    self.st.dataReady.connect(self.getWeight, QtCore.Qt.QueuedConnection)
    self.st.start()
    
  def addTransaction(self):
    if self.ticket.ticket_type_id == 1:
      transaction_type_id = 4
    else:
      transaction_type_id = 5
    self.api.get_warehouses()
    addTransactionDialog = AddTransaction(transaction_type_id, self)
    self.api.getWarehousesFinished.connect(addTransactionDialog.getWarehousesFinished)
    if addTransactionDialog.exec_() == QtGui.QDialog.Accepted:
      transaction = addTransactionDialog.transaction
      warehouse = addTransactionDialog.warehouse
      self.transactionsTableModel.addTransaction(transaction, warehouse)
    
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
    clientIndex = self.ui.clientsComboBox.currentIndex()
    clientListModel = self.ui.clientsComboBox.model()
    outgoing_weight = self.ui.outgoingWeightSpinBox.value()
    weight_captured = self.ui.captureWeightButton.isChecked()
    manualEnabled = self.ui.manualCheckBox.isChecked()
    net_weight = self.ui.netWeightSpinBox.value()
    provider_weight = self.ui.providerWeightSpinBox.value()
    provider_document_number = self.ui.providerDocumentNumberLineEdit.text()
    transactions_total = self.ui.transactionsTotalSpinBox.value()
    
    errors = []
    if clientIndex == -1:
      errors.append('El cliente no ha sido seleccionado')
    if not weight_captured and not manualEnabled:
      errors.append('El peso de salida no ha sido capturado')
    if not (net_weight - self.tolerance < transactions_total < net_weight + self.tolerance):
      errors.append('El total de transacciones se encuentra fuera de la tolerancia del peso neto')
    if self.ticket.ticket_type_id == 1:
      if provider_weight == 0:
        errors.append('El peso del proveedor no ha sido indicado')
      if provider_document_number == '':
        errors.append(u'El número de guía no ha sido indicado')
        
    if not errors:
      self.ticket.comment = self.ui.commentPlainTextEdit.toPlainText()
      self.ticket.outgoing_weight = outgoing_weight
      if self.ticket.ticket_type_id == 1:
        self.ticket.provider_weight = provider_weight
        self.ticket.provider_document_number = provider_document_number
      self.ticket.transactions_attributes = self.transactionsTableModel.getTransactions()
      client_id = clientListModel.getClient(clientIndex).id
      self.ticket.client_id = client_id
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
    if self.ticket.ticket_type_id == 2:
      gross_weight = weight
      tare_weight = self.ticket.incoming_weight
    else:
      gross_weight = self.ticket.incoming_weight
      tare_weight = weight
    net_weight = gross_weight - tare_weight
    self.ui.grossWeightSpinBox.setValue(gross_weight)
    self.ui.tareWeightSpinBox.setValue(tare_weight)
    self.ui.netWeightSpinBox.setValue(net_weight)
      
  def getClientsFinished(self, clients):
    self.clientsListModel = ClientsListModel(clients, self)
    self.ui.clientButton.setEnabled(True)

  def getFactoriesFinished(self, factories):
    self.factoriesListModel = ClientsListModel(factories, self)
    self.ui.factoryButton.setEnabled(True)
    
  def showClients(self):
    self.ui.clientsComboBox.setModel(self.clientsListModel)
    clientsLineEdit = self.ui.clientsComboBox.lineEdit()
    clientsLineEdit.setPlaceholderText('Seleccione un cliente')
    self.ui.clientsComboBox.setCurrentIndex(-1)
    
  def showFactories(self):
    self.ui.clientsComboBox.setModel(self.factoriesListModel)
    clientsLineEdit = self.ui.clientsComboBox.lineEdit()
    clientsLineEdit.setPlaceholderText(u'Seleccione una fábrica')
    self.ui.clientsComboBox.setCurrentIndex(-1)
    
class ClientsListModel(QtCore.QAbstractListModel):
  def __init__(self, clients, parent):
    super(ClientsListModel, self).__init__(parent)
    self._clients = clients
    
  def refreshClients(self, clients):
    self.beginResetModel()
    self._clients = clients
    self.endResetModel()
  
  def getClient(self, row):
    return self._clients[row]
  
  def rowCount(self, parent):
    return len(self._clients)
    
  def data(self, index, role):
    row = index.row()
    if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
      return self._clients[row].name

class TransactionsTableModel(QtCore.QAbstractTableModel):
  totalChanged = QtCore.Signal(float)
  def __init__(self, transactions, warehouses, parent):
    super(TransactionsTableModel, self).__init__(parent)
    self._transactions = transactions
    self._warehouses = warehouses
    self._headers = [u'Lote', u'Código', 'Nombre', 'Sacos', 'Kg/Saco', 'Cantidad']
    
  def getTransactions(self):
    return self._transactions
  
  def addTransaction(self, transaction, warehouse):
    row = len(self._warehouses)
    self.beginInsertRows(QtCore.QModelIndex(), row, row)
    self._transactions.append(transaction)
    self._warehouses.append(warehouse)
    self.endInsertRows()
    self._recalculateTotal()
  
  def removeTransaction(self, row):
    #self.beginRemoveRows(QtCore.QModelIndex(), row, 1)
    self.beginResetModel()
    transaction = self._transactions[row]
    warehouse = self._warehouses[row]
    self._transactions.remove(transaction)
    self._warehouses.remove(warehouse)
    #self.endRemoveRows()
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
    return len(self._warehouses)
    
  def columnCount(self, parent):
    return len(self._headers)
    
  def data(self, index, role):
    row = index.row()
    column = index.column()
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._warehouses[row].lot_code
      elif column == 1:
        return self._warehouses[row].content_code
      elif column == 2:
        return self._warehouses[row].content_name
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
