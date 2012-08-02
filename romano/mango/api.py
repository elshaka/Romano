# -*- coding: utf-8 -*-

from PySide import QtCore, QtNetwork
from mango.models.user import User
from mango.models.ticket import Ticket
from mango.models.driver import Driver
from mango.models.truck import Truck
from mango.models.client import Client
from mango.models.warehouse import Warehouse

class API(QtCore.QObject):
  loginFinished = QtCore.Signal()
  createTicketFinished = QtCore.Signal()
  getTicketsFinished = QtCore.Signal(list)
  getDriversFinished = QtCore.Signal(list)
  getTrucksFinished = QtCore.Signal(list)
  getClientsFinished = QtCore.Signal(list)
  getFactoriesFinished = QtCore.Signal(list)
  getWarehousesFinished = QtCore.Signal(list)
  closeTicketFinished = QtCore.Signal()
  printTicketFinished = QtCore.Signal(QtCore.QByteArray)
  
  def __init__(self, host = "localhost", port = 3000):
    super(API, self).__init__()
    self.manager = QtNetwork.QNetworkAccessManager()
    self.host = host
    self.port = port
    
  def _new_request(self, path):
    url = QtCore.QUrl("http://"+self.host+":"+str(self.port)+"/"+path)
    request = QtNetwork.QNetworkRequest(url)
    request.setHeader(request.ContentTypeHeader, "application/json")
    request.setRawHeader("Accept", "application/json")
    return request
    
  def login(self, username, password):
    request = self._new_request("sessions")
    data = QtCore.QByteArray("{\"user\":{\"login\":\""+username+"\", \"password\":\""+password+"\"}}")
    self.loginReply = self.manager.post(request, data)
    self.loginReply.finished.connect(self.login_finished)
    
  def login_finished(self):
    self.user = User.fromJSON(self.loginReply.readAll().data())
    self.loginFinished.emit()
    
  def get_tickets(self):
    request = self._new_request("tickets")
    self.getTicketsReply = self.manager.get(request)
    self.getTicketsReply.finished.connect(self.get_tickets_finished)
    
  def get_tickets_finished(self):
    tickets = Ticket.fromJSON(self.getTicketsReply.readAll().data())
    self.getTicketsFinished.emit(tickets)
    
  def get_drivers(self):
    request = self._new_request("drivers")
    self.getDriversReply = self.manager.get(request)
    self.getDriversReply.finished.connect(self.get_drivers_finished)
  
  def get_drivers_finished(self):
    drivers = Driver.fromJSON(self.getDriversReply.readAll().data())
    self.getDriversFinished.emit(drivers)

  def get_trucks(self):
    request = self._new_request("trucks")
    self.getTrucksReply = self.manager.get(request)
    self.getTrucksReply.finished.connect(self.get_trucks_finished)
  
  def get_trucks_finished(self):
    trucks = Truck.fromJSON(self.getTrucksReply.readAll().data())
    self.getTrucksFinished.emit(trucks)
    
  def create_ticket(self, ticket):
    request = self._new_request("tickets")
    data = QtCore.QByteArray(ticket.toJSON())
    self.createTicketReply = self.manager.post(request, data)
    self.createTicketReply.finished.connect(self.create_ticket_finished)
    
  def create_ticket_finished(self):
    self.createTicketFinished.emit()

  def get_clients(self):
    request = self._new_request("clients")
    self.getClientsReply = self.manager.get(request)
    self.getClientsReply.finished.connect(self.get_clients_finished)
    
  def get_clients_finished(self):
    clients = Client.fromJSON(self.getClientsReply.readAll().data())
    self.getClientsFinished.emit(clients)
    
  def get_factories(self):
    request = self._new_request("factories")
    self.getFactoriesReply = self.manager.get(request)
    self.getFactoriesReply.finished.connect(self.get_factories_finished)
    
  def get_factories_finished(self):
    factories = Client.fromJSON(self.getFactoriesReply.readAll().data())
    self.getFactoriesFinished.emit(factories)

  def close_ticket(self, ticket):
    request = self._new_request("tickets/%s" % ticket.id)
    _ticket = Ticket(ticket.ticket_type_id, ticket.driver_id, 
                     ticket.truck_id, ticket.incoming_weight,
                     ticket.comment)
    _ticket.outgoing_weight = ticket.outgoing_weight
    _ticket.provider_weight = ticket.provider_weight
    _ticket.provider_document_number = ticket.provider_document_number
    _ticket.client_id = ticket.client_id
    _ticket.transactions_attributes = ticket.transactions_attributes
    data = QtCore.QByteArray(_ticket.toJSON())
    self.closeTicketReply = self.manager.put(request, data)
    self.closeTicketReply.finished.connect(self.close_ticket_finished)
  
  def close_ticket_finished(self):
    self.closeTicketFinished.emit()
    
  def print_ticket(self, ticket):
    request = self._new_request("tickets/%s/print" % ticket.id)
    self.printTicketReply = self.manager.get(request)
    self.printTicketReply.finished.connect(self.print_ticket_finished)
    
  def print_ticket_finished(self):
    data = self.printTicketReply.readAll()
    self.printTicketFinished.emit(data)
  
  def get_warehouses(self):
    request = self._new_request("warehouses")
    self.getWarehousesReply = self.manager.get(request)
    self.getWarehousesReply.finished.connect(self.get_warehouses_finished)
    
  def get_warehouses_finished(self):
    warehouses = Warehouse.fromJSON(self.getWarehousesReply.readAll().data())
    self.getWarehousesFinished.emit(warehouses)
