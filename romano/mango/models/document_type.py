from .jsonable import JSONableModel

class DocumentType(JSONableModel):
  def __init__(self, name):
    self.name = name

  @classmethod
  def fromDict(cls, dict_):
    document_type = cls(dict_['name'])
    document_type.id = dict_['id']
    return document_type
