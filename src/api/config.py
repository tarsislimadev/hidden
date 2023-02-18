import os

data_path=os.getenv('DATA_PATH', '/data')

host=os.getenv('HOST', '127.0.0.1')

port=int(os.getenv('PORT', '80'))
