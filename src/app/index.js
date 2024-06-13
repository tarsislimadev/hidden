import { Server } from '@brtmvdl/backend'

import { PORT } from './config.js'

const server = new Server()

server.get('*', (req, res) => { console.log({ req, res }); return res })

server.listen(PORT)
