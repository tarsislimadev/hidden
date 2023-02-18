from json import JSONDecoder
from libs.logger.logger import log

class Request:
  def __init__(self, client):
    log('libs/http/Request', client)
    self.chunk = str(client.recv(1024).decode('ascii'))

  def getLines(self):
    log('libs/http/Request/getLines', None)
    return self.chunk.splitlines()

  def getFirstLine(self):
    log('libs/http/Request/getFirstLine', None)
    lines = self.getLines()
    return lines[0].split(' ')

  def getMethod(self):
    log('libs/http/Request/getMethod', None)
    firstLine = self.getFirstLine()
    return firstLine[0]

  def getFullPath(self):
    log('libs/http/Request/getFullPath', None)
    firstLine = self.getFirstLine()
    return firstLine[1]

  def getPath(self):
    log('libs/http/Request/getPath', None)
    fullpath = self.getFullPath()
    parts = fullpath.split('?', 2)
    return parts[0][1:]

  def getQueries(self):
    log('libs/http/Request/getQueries', None)
    fullpath = self.getFullPath()
    parts = fullpath.split('?', 2)

    if (len(parts) == 2):
      return map(lambda x: x.split('=', 2), parts[1].split('&'))

    return []

  def getQuery(self, name):
    log('libs/http/Request/getQuery', name)
    return self.getQueries()[name]

  def getHeaders(self):
    log('libs/http/Request/getHeaders', None)
    lines = self.getLines()
    return lines[1:-1]

  def getBody(self):
    log('libs/http/Request/getBody', None)
    lines = self.getLines()
    body = JSONDecoder().decode(lines[lines.__len__() - 1])
    print("body: ", body)
    return body

  def __str__(self):
    return self.chunk
