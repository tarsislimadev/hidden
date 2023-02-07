
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

const goTo = (location, value = null) => (window.location = location)

const l = new Local('api')

const API = {}

API.listPosts = () => l.get(['posts'], [])

API.savePost = (post) => l.add(['posts'], post)
