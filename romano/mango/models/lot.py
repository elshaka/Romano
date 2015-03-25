from .jsonable import JSONableModel

class Lot(JSONableModel):
  def __init__(self, code, stock, comment):
    self.code = code
    self.stock = stock
    self.comment = comment
  
  @classmethod
  def fromDict(cls, dict_):
    lot = cls(dict_['code'], dict_['stock'], dict_['comment'])
    lot.id = dict_['id']
    lot.content_name = dict_['get_content']['ingredient']['name']
    lot.content_code = dict_['get_content']['ingredient']['code']
    return lot
