import { HTML, nFlex, nH1, nLink, nError } from '@brtmvdl/frontend'

import { API, goTo } from './js/api.js'

const app = HTML.fromId('app')

const head = new nFlex()
head.setStyle('padding', '1rem')
app.append(head)

const title = new nH1()
title.setStyle('text-align', 'center')
title.setText('Hidden')
head.append(title)

const headButton = new nLink()
headButton.href('create.html')
headButton.setStyle('line-height', '3rem')
headButton.setStyle('font-size', '3rem')
headButton.setStyle('height', '3rem')
headButton.setStyle('width', '3rem')
headButton.setText('+')
head.append(headButton)

const errorMessage = new nError()
app.append(errorMessage)

const list = new HTML()
list.setStyle('padding', '1rem')
app.append(list)

const parseColor = (color) => {
  switch (color) {
    case 'red': return 'black';
    case 'black': return 'white';
  }

  return 'black'
}

const renderPost = ({ id, color, text, likes }) => {
  // const width = ((window.innerWidth - 32) / 1) + 'px'

  const post = new HTML()
  post.setStyle('background-color', 'blue')
  post.setStyle('margin-bottom', '1rem')
  post.setStyle('text-align', 'center')
  post.setStyle('padding', '1rem')

  const postText = new HTML()
  postText.setText(text)
  post.append(postText)

  list.append(post)
}

API.listPosts()
  .then((res) => res.get('list', []).map((post, id) => renderPost({ id, ...post })))
  .catch((err) => errorMessage.setText(err.message))

API.sync()

setInterval(() => API.sync(), 60 * 1000)
