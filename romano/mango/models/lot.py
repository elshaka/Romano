from .jsonable import JSONableModel

class Lot(JSONableModel):
  def __init__(self, code, stock, location):
    self.code = code
    self.stock = stock
    self.location = location
  
  @classmethod
  def fromDict(cls, dict_):
    lot = cls(dict_['code'], dict_['code'], dict_['location'])
    lot.id = dict_['id']
    lot.content_name = dict_['get_content']['ingredient']['name']
    lot.content_code = dict_['get_content']['ingredient']['code']
    return lot
