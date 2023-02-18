import os
import uuid
from libs.logger.logger import log
from json import JSONEncoder

class DatabaseObject:
  def __init__(self, path: str, id = uuid.uuid4().__str__()):
    log('libs/database/DatabaseObject', {path, id})
    self.path = path
    self.id = id
    self.fullPath = '/'.join([path, id])
    os.makedirs(self.fullPath, exist_ok=True)

  def getPropName(self, name: str):
    return '/'.join([self.fullPath, name])

  def writeMany(self, props = []):
    log('libs/database/DatabaseObject:writeMany', props)
    for value, name  in props:
      self.write(name, value)
    return self

  def write(self, name, value = ''):
    log('libs/database/DatabaseObject:write', {name, value})
    f = open(self.getPropName(name), 'w+')
    f.write(value)
    f.close()
    return self

  def getProps(self):
    return os.listdir(self.fullPath)

  def read(self, name):
    f = open(self.getPropName(name), 'r+')
    content = f.read()
    f.close()
    return content
  
  def __str__(self):
    props = {}

    for prop in self.getProps():
      props[prop] = self.read(prop)

    return str(props)
