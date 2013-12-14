from .jsonable import JSONableModel

class Driver(JSONableModel):
  def __init__(self, ci, name, address, tel1, tel2):
    self.ci = ci
    self.name = name
    self.address = address
    self.tel1 = tel1
    self.tel2 = tel2
    self.frequent = False
  
  @classmethod
  def fromDict(cls, dict_):
    driver = cls(dict_['ci'], dict_['name'], dict_['address'],
                 dict_['tel1'], dict_['tel2'])
    driver.id = dict_['id']
    return driver
