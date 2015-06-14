import simplejson as json

class JSONableModel:
  def jsonable(self):
    return self.__dict__

  def toJSON(self):
    classname = toClassname(self.__class__.__name__)
    return '{"%s":%s}' % (classname, json.dumps(self, cls = CustomEncoder))

  @classmethod
  def fromJSON(cls, json_string):
    parsed = json.loads(json_string)
    classname = toClassname(cls.__name__)
    if isinstance(parsed, list):
      return list(map((lambda i: cls.fromDict(i[classname])), parsed))
    else:
      return cls.fromDict(parsed[classname])

  @classmethod
  def fromDict(cls, dict_):
    raise NotImplementedError

class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'jsonable'):
      return obj.jsonable()
    else:
      raise TypeError('Object %s is not JSON serializable' % obj)

def toClassname(string):
  classname = ""
  for char in string:
    if char.isupper():
      if classname != "":
        classname += "_"
      classname += char.lower()
    else:
      classname += char
  return classname
