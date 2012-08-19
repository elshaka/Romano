from jsonable import JSONableModel

class Carrier(JSONableModel):
  def __init__(self, name, rif):
    self.name = name
    self.rif = rif
    self.email = None
    self.tel1 = None
    self.tel2 = None
    self.address = None
    self.frequent = False
  
  @classmethod
  def fromDict(cls, dict_):
    carrier = cls(dict_['name'], dict_['rif'])
    carrier.id = dict_['id']
    carrier.code = dict_['code']
    carrier.email = dict_['email']
    carrier.tel1 = dict_['tel1']
    carrier.tel2 = dict_['tel2']
    carrier.address = dict_['address']
    return carrier
