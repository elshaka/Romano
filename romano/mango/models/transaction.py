from jsonable import JSONableModel

class Transaction(JSONableModel):
  def __init__(self, transaction_type_id, warehouse_id, sack, sack_weight,
               sacks, amount):
    self.transaction_type_id = transaction_type_id
    self.warehouse_id = warehouse_id
    self.sack = sack
    self.sack_weight = sack_weight
    self.sacks = sacks
    self.amount = amount
