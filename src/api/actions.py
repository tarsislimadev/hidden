import config
from libs.database.Database import Database

db = Database(config.data_path)

def Sync(req, res):
  body = req.getBody()
  posts = db.index('posts')

  for post in body['list']:
    print('post: ', post)
    posts.new().write('text', post['text'])

  return res.setJSON({ 'list' : posts.list() })
