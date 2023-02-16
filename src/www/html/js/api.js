
class Response {
  constructor({ status, message, data } = {}) {
    this.status = status
    this.message = message
    this.data = data
  }

  getData() {
    return this.data || {}
  }

  get(name, other = '') {
    return this.getData()[name] || other
  }

  getMessage() {
    return this.message || null
  }

  getStatus() {
    return this.status
  }
}

class SuccessResponse extends Response {
  constructor(data = {}) {
    super({
      status: 'ok',
      message: null,
      data
    })
  }
}

class ErrorResponse extends Response {
  constructor(err = new Error) {
    super({
      status: 'error',
      message: err.message,
      data: { stack: err.stack }
    })
  }
}

const Local = function (id = '') {
  const self = this

  self.id = id

  self.named = (paths = []) => [self.id, ...paths].join('.')

  self.get = function (paths = [], def = null) {
    return new Promise((resolve) => {
      try {
        const local = localStorage.getItem(self.named(paths))
        resolve(new SuccessResponse(JSON.parse(local)))
      } catch (e) {
        console.error(e)
        resolve(def)
      }
    })
  }

  self.set = function (paths = [], data = {}) {
    return new Promise((resolve, reject) => {
      try {
        localStorage.setItem(self.named(paths), JSON.stringify(data))
        resolve(new SuccessResponse({}))
      } catch (e) {
        reject(new ErrorResponse(e))
      }
    })
  }

  self.add = async function (paths = [], data = {}) {
    const res = await this.get(paths)

    const list = res.get('list', [])

    list.push(data)

    return this.set(paths, { list })
  }
}

const Ajax = {}

Ajax.post = (url, data = {}) => {
  return new Promise((res, rej) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', url, true)

    const onComplete = (xhr) => xhr.status === '200'
      ? res(new SuccessResponse(xhr))
      : rej(new ErrorResponse(xhr))

    xhr.onerror = () => onComplete(xhr)
    xhr.onload = () => onComplete(xhr)

    xhr.send(JSON.stringify(data))
  })
}

const goBack = () => { window.history.back() }

const goTo = (location, value = null) => (window.location = location)

const API = {}

const l = new Local('api')

API.listPosts = () => l.get(['posts'], [])

API.savePost = (post) => l.add(['posts'], post)

API.saveHost = ({ host }) => l.add(['hosts'], { address: host })

API.getPosts = ({ address, posts }) => Ajax.post(`http://${address}/sync`, { list: posts })

API.sync = () => {
  l.get(['hosts'], [])
    .then((res) =>
      res.get('list', [])
        .map((host) => host.address || '')
        .filter((address) => !!address)
        .map((address) =>
          API.getPosts({ address, posts: API.listPosts() })
            .then((res) => {
              const list = res.get('list')
              console.log({ list })
            })
        )
    )
}
