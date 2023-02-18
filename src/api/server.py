import threading
import socket

import config
import actions

from libs.http.Request import Request
from libs.http.Response import Response

from libs.logger.logger import log

def listen():
  log('server:listen', None)
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((config.host, config.port))
  server.listen()

  while True:
    client, _ = server.accept()
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

def handle(client):
  log('server:handle', None)
  request = Request(client)
  response = str(run(request))

  client.send(str(response + '\r\n').encode('ascii'))
  client.close()

def run(request):
  log('server:run', request)
  response = Response(request)

  path = request.getPath()

  print("Path: " + path)

  match path:
    case 'sync':
      return actions.Sync(request, response)

  return response.setError('404', 'No route found.')

