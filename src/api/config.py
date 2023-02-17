import os

data_path=os.getenv('DATA_PATH', '/data')

host=os.getenv('host', '127.0.0.1')

port=int(os.getenv('PORT', '80'))

http = {
  'status': {
    'OK': '200',
    'CLIENT_ERROR': '400',
    'FORBIDDEN': '403',
    'NOT_FOUND': '404',
    'SERVER_ERROR': '500',
  },
  'path': {
    'SYNC': 'sync'
  }
}
