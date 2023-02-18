import os
from .DatabaseObject import DatabaseObject
from libs.logger.logger import log
import array

class Database:
  def __init__(self, path):
    log('libs/database/Database', path)
    self.path = path
    self.mkdir()

  def mkdir(self):
    log('libs/database/Database:mkdir', None)
    os.makedirs(self.path, exist_ok=True)
    return self

  def index(self, path):
    log('libs/database/Database:index', path)
    return Database('/'.join([self.path, path]))

  def list(self):
    log('libs/database/Database:list', None)
    listed = []
    files = os.listdir(self.path)

    for file in files:
      listed.append(DatabaseObject(self.path, file))

    return listed

  def new(self):
    log('libs/database/Database:new', None)
    return DatabaseObject(self.path)
