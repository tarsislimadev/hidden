from json import JSONEncoder
import threading
import socket

import config
import actions

class Request:
  def __init__(self, client) -> None:
    self.chunk = str(client.recv(1024).decode('ascii'))

  def getMethod(self):
    return ''
  
  def getPath(self):
    return ''
  
  def getQueries(self):
    return ''
  
  def getQuery(self, name):
    return ''

  def getHeaders(self):
    return ['']
  
  def getBody(self):
    return ''

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

  def __str__(self):
    res = []
    res.append('HTTP/1.1 200 OK')
    res.append('Content-Type: application/json')
    res.append('')
    res.append(JSONEncoder().encode(self.json))
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

  if (path == 'sync'):
    return actions.Sync(request, response)

  return response

