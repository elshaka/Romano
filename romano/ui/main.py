# -*- coding: utf-8 -*-

import os
import configparser
import dateutil.parser
from PySide import QtGui, QtCore
from .ui_main import Ui_Main
from .login import Login
from .new_ticket import NewTicket
from .close_ticket import CloseTicket
from mango.api import API

class Main(QtGui.QMainWindow):
  def __init__(self):
    super(Main, self).__init__()
    self.ui = Ui_Main()
    self.ui.setupUi(self)
    self.ticketsTableModel = TicketsTableModel([])
    self.ui.ticketsTableView.setModel(self.ticketsTableModel)
    horizontalHeader = self.ui.ticketsTableView.horizontalHeader()
    horizontalHeader.setResizeMode(QtGui.QHeaderView.ResizeToContents)
    config = configparser.ConfigParser()
    config.read('settings.ini')

    self.api = API(config.get('Server','Host'), config.getint('Server','Port'))
    self.ui.actionNewReception.triggered.connect(self.openTicket)
    self.ui.actionNewDispatch.triggered.connect(self.openTicket)
    self.ui.actionLogout.triggered.connect(self.logout)
    self.ui.refreshButton.clicked.connect(self.getTickets)
    self.api.getTicketsFinished.connect(self.getTicketsFinished)
    self.api.createTicketFinished.connect(self.getTickets)
    self.api.closeTicketFinished.connect(self.printTicket)
    self.api.printTicketFinished.connect(self.printTicketFinished)
    self.ui.ticketsTableView.doubleClicked.connect(self.closeTicket)

    self.login()

  def openTicket(self):
    actionSender = self.sender()
    if actionSender == self.ui.actionNewReception:
      newTicketDialog = NewTicket(1, self.user.allow_manual, self)
    elif actionSender == self.ui.actionNewDispatch:
      newTicketDialog = NewTicket(2, self.user.allow_manual, self)

    if newTicketDialog.exec_() == QtGui.QDialog.Accepted:
      self.api.create_ticket(newTicketDialog.ticket)
    newTicketDialog.st.alive = False

  def closeTicket(self, tableIndex):
    ticket = self.ticketsTableModel.getTicket(tableIndex.row())
    closeTicketDialog = CloseTicket(ticket, self.user.allow_manual, self)
    if closeTicketDialog.exec_() == QtGui.QDialog.Accepted:
      self.api.close_ticket(closeTicketDialog.ticket)
      self.currentTicket = closeTicketDialog.ticket
    closeTicketDialog.st.alive = False

  def printTicket(self):
    self.getTickets()
    self.api.print_ticket(self.currentTicket)

  def printTicketFinished(self, data):
    filename = QtCore.QDir.tempPath() + "/ticket_%s.pdf" % self.currentTicket.number
    _file = QtCore.QFile(filename)
    _file.open(QtCore.QIODevice.WriteOnly)
    _file.write(data)
    _file.close
    if os.name == "posix":
      os.system("xdg-open %s" % filename)
    elif os.name == "nt":
      os.startfile(filename)

  def login(self):
    loginDialog = Login(self.api, self)
    if loginDialog.exec_() == QtGui.QDialog.Accepted:
      self.user = loginDialog.user
      self.ui.refreshButton.setEnabled(False)
      self.api.get_tickets()
      
      self.ui.actionUserName.setText(self.user.name)
      self.center()
      self.show()
    else:
      self.close()
      
  def logout(self):
    self.hide()
    self.login()

  def getTickets(self):
    self.ui.refreshButton.setEnabled(False)
    self.api.get_tickets()
  
  def getTicketsFinished(self, tickets):
    self.ui.ticketsTableView.model().refreshTickets(tickets)
    self.ui.refreshButton.setEnabled(True)
    
  def center(self):
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
    
class TicketsTableModel(QtCore.QAbstractTableModel):
  def __init__(self, tickets, parent = None):
    super(TicketsTableModel, self).__init__(parent)
    self._tickets = tickets
    self._headers = ['Número', 'Tipo', 'Chofer', 'Placa', 'Peso de entrada', 'Fecha de entrada', 'Comentario']
    
  def getTicket(self, row):
    return self._tickets[row]
    
  def refreshTickets(self, tickets):
    self.beginResetModel()
    self._tickets = tickets
    self.endResetModel()
    
  def headerData(self, section, orientation, role):
    if role == QtCore.Qt.DisplayRole:
      if orientation == QtCore.Qt.Horizontal:
        return self._headers[section]
        
  def rowCount(self, parent):
    return len(self._tickets)
    
  def columnCount(self, parent):
    return len(self._headers)
    
  def data(self, index, role):
    row = index.row()
    column = index.column()
    
    if role == QtCore.Qt.DisplayRole:
      if column == 0:
        return self._tickets[row].number
      elif column == 1:
        return self._tickets[row].ticket_type.code
      elif column == 2:
        return self._tickets[row].driver.name
      elif column == 3:
        return self._tickets[row].truck.license_plate
      elif column == 4:
        return "%s Kg" % self._tickets[row].incoming_weight
      elif column == 5:
        return dateutil.parser.parse(self._tickets[row].incoming_date).strftime("%Y/%m/%d %I:%M:%S %p")
      elif column == 6:
        return self._tickets[row].comment
    elif role == QtCore.Qt.TextAlignmentRole:
      if column == 4:
        return QtCore.Qt.AlignRight
      elif column == 6:
        return QtCore.Qt.AlignLeft
      else:
        return QtCore.Qt.AlignCenter
