from .jsonable import JSONableModel
from .driver import Driver
from .truck import Truck
from .ticket_type import TicketType

class Ticket(JSONableModel):
  def __init__(self, ticket_type_id, driver_id, truck_id,
               incoming_weight, comment):
    self.ticket_type_id = ticket_type_id
    self.driver_id = driver_id
    self.truck_id = truck_id
    self.incoming_weight = incoming_weight
    self.comment = comment
    self.manual_incoming = False
    self.manual_outgoing = False

  @classmethod
  def fromDict(cls, dict_):
    ticket_type = TicketType.fromDict(dict_['ticket_type'])
    driver = Driver.fromDict(dict_['driver'])
    truck = Truck.fromDict(dict_['truck'])
    ticket = cls(dict_['ticket_type_id'], dict_['driver_id'], 
                 dict_['truck_id'], dict_['incoming_weight'],
                 dict_['comment'])
    ticket.id = dict_['id']
    ticket.number = dict_['number']
    ticket.incoming_date = dict_['incoming_date']
    ticket.provider_weight = dict_['provider_weight']
    ticket.provider_document_number = dict_['provider_document_number']
    ticket.manual_incoming = dict_['manual_incoming']
    ticket.manual_outgoing = dict_['manual_outgoing']
    ticket.ticket_type = ticket_type
    ticket.driver = driver
    ticket.truck = truck
    return ticket
