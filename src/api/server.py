from json import JSONEncoder
import threading
import socket

import config
import actions

class Request:
  def __init__(self, client) -> None:
    self.chunk = str(client.recv(1024).decode('ascii'))

  def getLines(self):
    return self.chunk.splitlines()

  def getFirstLine(self):
    lines = self.getLines()
    return lines[0].split(' ')

  def getMethod(self):
    firstLine = self.getFirstLine()
    return firstLine[0]

  def getPath(self):
    firstLine = self.getFirstLine()
    return firstLine[1] # FIXME

  def getQueries(self):
    firstLine = self.getFirstLine()
    return firstLine[1] # FIXME

  def getQuery(self, name):
    return self.getQueries()[name]

  def getHeaders(self):
    headers = []
    return headers # FIXME

  def getBody(self):
    body = ''
    return body # FIXME

  def __str__(self):
    return self.chunk

class Response():
  def __init__(self, request) -> None:
    self.request = request
    self.status = '200'
    self.headers = []
    self.json = {
      'status': 'ok',
      'message': '',
      'body': {}
    }

  def setJSON(self, json = {}):
    self.status = '200'
    self.json.status = 'ok'
    self.json.message = ''
    self.json.body = json 
    return self

  def setError(self, message):
    self.status = '404'
    self.json.status = 'error'
    self.json.message = message
    self.json.body = {}
    return self
  
  def getStatusMessage(self, status):
    if status == config.http.status.OK:
      return 'OK'

    if status == config.http.status.NOT_FOUND:
      return 'NOT FOUND'

    return 'ERROR'
  
  def getFirstLine(self, status):
    message = self.getStatusMessage(status)
    return ' '.join(['HTTP/1.1', status, message])

  def parseHeader(name, value = ''):
    return ': '.join([name, value])
  
  def getBodyString(self):
    return JSONEncoder().encode(self.json)

  def __str__(self):
    res = []

    # res.append('HTTP/1.1 200 OK')
    res.append(self.getFirstLine('200'))

    # res.append('Content-Type: application/json')
    res.append(self.parseHeader('Content-Type', 'application/json'))

    res.append('')

    # res.append(JSONEncoder().encode(self.json))
    res.append(self.getBodyString())

    res.append('')

    return str('\r\n'.join(res))

def listen():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((config.host, config.port))
  server.listen()

  while True:
    client, _ = server.accept()
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

def handle(client):
  request = Request(client)
  print(request.__str__())

  response = run(request)
  print(response.__str__())

  client.send(str(response.__str__() + '\r\n').encode('ascii'))
  client.close()

def run(request):
  response = Response(request)

  path = request.getPath()

  if (path == config.http.path.SYNC):
    return actions.Sync(request, response)

  return response
