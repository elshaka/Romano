from jsonable import JSONableModel

class Driver(JSONableModel):
  def __init__(self, id, ci, name, address, tel1, tel2):
    self.id = id
    self.ci = ci
    self.name = name
    self.address = address
    self.tel1 = tel1
    self.tel2 = tel2
  
  @classmethod
  def fromDict(cls, dict_):
    driver = cls(dict_['id'], dict_['ci'], dict_['name'], 
                 dict_['address'], dict_['tel1'], dict_['tel2'])
    return driver
