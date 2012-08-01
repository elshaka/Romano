from jsonable import JSONableModel

class Warehouse(JSONableModel):
  def __init__(self, warehouse_type_id, content_id, code, stock, location):
    self.warehouse_type_id = warehouse_type_id
    self.content_id = content_id
    self.code = code
    self.stock = stock
    self.location = location
  
  @classmethod
  def fromDict(cls, dict_):
    warehouse = cls(dict_['warehouse_type_id'], dict_['content_id'],
                    dict_['code'], dict_['stock'], dict_['location'])
    warehouse.id = dict_['id']
    warehouse.content_code = dict_['content_code']
    warehouse.content_name = dict_['content_name']
    warehouse.lot_code = dict_['lot_code']
    return warehouse
