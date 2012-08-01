from jsonable import JSONableModel

class TicketType(JSONableModel):
  def __init__(self, id, code, description):
    self.id = id
    self.code = code
    self.description = description
    
  @classmethod
  def fromDict(cls, dict_):
    ticket_type = cls(dict_['id'], dict_['code'], dict_['description'])
    return ticket_type
