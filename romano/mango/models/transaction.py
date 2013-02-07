from jsonable import JSONableModel

class Transaction(JSONableModel):
  def __init__(self, transaction_type_id, content_type, content_id, sack, sack_weight,
               sacks, amount):
    self.transaction_type_id = transaction_type_id
    self.content_type = content_type
    self.content_id = content_id
    self.sack = sack
    self.sack_weight = sack_weight
    self.sacks = sacks
    self.amount = amount
    self.processed_in_stock = True
