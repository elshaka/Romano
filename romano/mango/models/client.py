from .jsonable import JSONableModel

class Client(JSONableModel):
  def __init__(self, code, ci_rif, name, tel1, address):    
    self.code = code
    self.ci_rif = ci_rif
    self.name = name
    self.tel1 = tel1
    self.address = address

  @classmethod
  def fromDict(cls, dict_):
    client = cls(dict_['code'], dict_['ci_rif'],  dict_['name'], 
                 dict_['tel1'], dict_['address'])
    client.tel2 = dict_['tel2']
    client.id = dict_['id']
    return client
