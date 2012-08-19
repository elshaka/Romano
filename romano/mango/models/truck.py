from jsonable import JSONableModel
from carrier import Carrier

class Truck(JSONableModel):
  def __init__(self, carrier_id, license_plate):
    self.carrier_id = carrier_id
    self.license_plate = license_plate
    self.frequent = False
    
  @classmethod
  def fromDict(cls, dict_):
    truck = cls(dict_['carrier_id'], dict_['license_plate'])
    truck.carrier = Carrier.fromDict(dict_['carrier'])
    truck.id = dict_['id']
    return truck
