from jsonable import JSONableModel
from carrier import Carrier

class Truck(JSONableModel):
  def __init__(self, id, carrier_id, license_plate, carrier):
    self.id = id
    self.carrier_id = carrier_id
    self.license_plate = license_plate
    self.carrier = carrier
    
  @classmethod
  def fromDict(cls, dict_):
    carrier = Carrier.fromDict(dict_['carrier'])
    truck = cls(dict_['id'], dict_['carrier_id'], dict_['license_plate'], carrier)
    return truck
