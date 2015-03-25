from .jsonable import JSONableModel

class Settings(JSONableModel):
  def __init__(self, ticket_reception_diff, ticket_dispatch_diff):    
    self.ticket_reception_diff = ticket_reception_diff
    self.ticket_dispatch_diff = ticket_dispatch_diff

  @classmethod
  def fromDict(cls, dict_):
    settings = cls(dict_['ticket_reception_diff'], dict_['ticket_dispatch_diff'])
    return settings
