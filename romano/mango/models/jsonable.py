import simplejson as json

class JSONableModel:
  def jsonable(self):
    return self.__dict__
  
  def toJSON(self):
    classname = self.__class__.__name__.lower() 
    return '{"%s":%s}' % (classname, json.dumps(self, cls = CustomEncoder))
  
  @classmethod
  def fromJSON(cls, json_string):    
    decoded = json.loads(json_string)
    classname = cls.__name__.lower()
    if isinstance(decoded, list):
      instances = []
      for item in decoded:
        instances.append(cls.fromDict(item[classname]))
      return instances
    else:
      return cls.fromDict(decoded[classname])
  
  @classmethod
  def fromDict(cls, dict_):
    raise NotImplementedError
    
class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'jsonable'):
      return obj.jsonable()
    else:
      raise TypeError, 'Object %s is not JSON serializable' % obj
