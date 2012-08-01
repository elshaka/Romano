from jsonable import JSONableModel

class Transaction(JSONableModel):
  def __init__(self, transaction_type_id, warehouse_id, amount):
    self.transaction_type_id = transaction_type_id
    self.warehouse_id = warehouse_id
    self.amount = amount
