from .jsonable import JSONableModel

class User(JSONableModel):
  def __init__(self, login, name):
    self.login = login
    self.name = name
    
  @classmethod
  def fromDict(cls, dict_):
    user = cls(dict_['login'], dict_['name'])
    user.id = dict_['id']
    user.allow_manual = dict_['allow_manual']
    return user
