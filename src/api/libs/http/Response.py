from json import JSONEncoder, JSONDecoder
from libs.logger.logger import log

class Response():
  def __init__(self, request):
    log('libs/http/Response', request)
    self.request = request
    self.status = '200'
    self.headers = []
    self.json = {
      'status': 'ok',
      'message': '',
      'data': {},
    }

  def setJSON(self, json = {}):
    log('libs/http/Response/setJSON', json)
    self.status = '200'
    self.json = {
      'status': 'ok',
      'message': '',
      'data': json,
    }
    return self

  def setError(self, status = '400', message = ''):
    log('libs/http/Response/setError', {status, message})
    self.status = status
    self.json = {
      'status': 'error',
      'message': message,
      'data': {},
    }
    return self
  
  def getStatusMessage(self, status):
    log('libs/http/Response/getStatusMessage', status)
    if status == '200':
      return 'OK'

    if status == '404':
      return 'NOT FOUND'

    return 'ERROR'
  
  def getFirstLine(self, status):
    log('libs/http/Response/getFirstLine', status)
    message = self.getStatusMessage(status)
    return ' '.join(['HTTP/1.1', status, message])

  def getBodyString(self):
    log('libs/http/Response/getBodyString', self.json)
    return str(self.json)

  def __str__(self):
    res = []

    res.append(self.getFirstLine(self.status))
    res.append(': '.join(['Content-Type', 'application/json']))
    res.append('')
    res.append(self.getBodyString())

    res.append('')

    return str('\r\n'.join(res))
