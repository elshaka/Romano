from jsonable import JSONableModel

class Carrier(JSONableModel):
  def __init__(self, id, code, name, rif):
    self.id = id
    self.code = code
    self.name = name
    self.rif = rif
    self.email = None
    self.tel1 = None
    self.tel2 = None
    self.address = None
  
  @classmethod
  def fromDict(cls, dict_):
    carrier = cls(dict_['id'], dict_['code'], dict_['name'], dict_['rif'])
    carrier.email = dict_['email']
    carrier.tel1 = dict_['tel1']
    carrier.tel2 = dict_['tel2']
    carrier.address = dict_['address']
    return carrier
