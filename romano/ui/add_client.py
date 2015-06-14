# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from .ui_add_client import Ui_AddClient
from mango.models.client import Client
from .error_message_box import ErrorMessageBox
from .error_message_box import NewErrorMessageBox

class AddClient(QtGui.QDialog):
  def __init__(self, parent):
    super(AddClient, self).__init__(parent)
    self.ui = Ui_AddClient()
    self.ui.setupUi(self)
    self.api = parent.api
    self.api.get_clients()
    self.api.get_factories()
    #self.ui.newWidget.setEnabled(False)
    #self.ui.newWidget.hide()
    self.ui.saveAsFactoryBox.hide()
    #self.ui.widget.hide()
    #self.ui.line.hide()

    self.clientsTableModel = ClientsTableModel([], self)
    self.factoriesTableModel = ClientsTableModel([], self)
    self.filterClientsProxyModel = QtGui.QSortFilterProxyModel()
    self.filterClientsProxyModel.setSourceModel(self.clientsTableModel)
    self.filterClientsProxyModel.setFilterKeyColumn(-1)
    self.filterClientsProxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    self.ui.clientsTableView.setModel(self.filterClientsProxyModel)
    self.ui.filterLineEdit.textChanged.connect(self.filterClientsProxyModel.setFilterRegExp)

    self.api.getClientsFinished.connect(self.getClientsFinished)
    self.api.getFactoriesFinished.connect(self.getFactoriesFinished)
    self.ui.newButton.clicked.connect(self.enableClientType)
    self.ui.existingButton.clicked.connect(self.enableClientType)
    self.ui.clientButton.clicked.connect(self.showClients)
    self.ui.factoryButton.clicked.connect(self.showFactories)
    self.ui.addButton.clicked.connect(self.addClient)
    self.ui.clientsTableView.doubleClicked.connect(self.addClient)
    self.ui.cancelButton.clicked.connect(self.reject)

  def addClient(self):
    if self.ui.newButton.isChecked():
      errors = []
      code = self.ui.codeLineEdit.text()
      ci_rif = self.ui.cirifLineEdit.text()
      name = self.ui.nameLineEdit.text()
      tel1 = self.ui.telLineEdit.text()
      address = self.ui.addressLineEdit.text()
      factory = self.ui.saveAsFactoryBox.isChecked()

      client = Client(code, ci_rif, name, tel1, address)
      client.factory = factory
      self.api.create_client(client)
      self.api.createClientFinished.connect(self.createClientFinished)
      self.api.createClientFailed.connect(self.createClientFailed)
    else:
      errors = []
      clientsModel = self.filterClientsProxyModel.sourceModel()
      clientFilteredIndex = self.ui.clientsTableView.currentIndex()
      if clientFilteredIndex.row() == -1:
        errors.append("Debe seleccionar un cliente")
      if not errors:
        clientIndex = self.filterClientsProxyModel.mapToSource(clientFilteredIndex)
        self.client = clientsModel.getClient(clientIndex.row())
        self.accept()
      else:
        ErrorMessageBox(errors).exec_()

  def createClientFinished(self, client):
    self.client = client
    self.accept()

  def createClientFailed(self, errors):
    NewErrorMessageBox(errors).exec_()

  def enableClientType(self):
    if self.ui.newButton.isChecked():
      self.ui.newWidget.setEnabled(True)
      self.ui.existingWidget.setEnabled(False)
    else:
      self.ui.newWidget.setEnabled(False)
      self.ui.existingWidget.setEnabled(True)

  def showClients(self):
    self.filterClientsProxyModel.setSourceModel(self.clientsTableModel)

  def showFactories(self):
    self.filterClientsProxyModel.setSourceModel(self.factoriesTableModel)
    
  def getClientsFinished(self, clients):
    self.clientsTableModel.refreshClients(clients)
    self.ui.clientButton.setEnabled(True)

  def getFactoriesFinished(self, factories):
    self.factoriesTableModel.refreshClients(factories)
    self.ui.factoryButton.setEnabled(True)

class ClientsTableModel(QtCore.QAbstractTableModel):
  def __init__(self, clients, parent):
    super(ClientsTableModel, self).__init__(parent)
    self._clients = clients
    self._headers = ['Código', 'Nombre']

  def getClient(self, row):
    return self._clients[row]

  def refreshClients(self, clients):
    self.beginResetModel()
    self._clients = clients
    self.endResetModel()

  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]

  def rowCount(self, parent):
    return len(self._clients)

  def columnCount(self, parent):
    return len(self._headers)

  def data(self, index, role):
    row = index.row()
    column = index.column()

    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._clients[row].code
      elif column == 1:
        return self._clients[row].name
