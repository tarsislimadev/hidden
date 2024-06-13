import { HTML, nFlex, nH1, nLink, nError, nInputText, nButton } from '@brtmvdl/frontend'

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
headButton.href('index.html')
headButton.setStyle('line-height', '3rem')
headButton.setStyle('font-size', '3rem')
headButton.setStyle('height', '3rem')
headButton.setStyle('width', '3rem')
headButton.setText('-')
head.append(headButton)

const errorMessage = new nError()
app.append(errorMessage)

const input = new nInputText()
input.setStyle('background-color', 'black')
input.setStyle('text-align', 'center')
input.setStyle('font', 'inherit')
input.setStyle('height', '20rem')
input.setStyle('color', 'white')
input.element.focus()
app.append(input)

const button = new nButton()
button.setStyle('width', '100%')
button.setText('save')
button.on('click', () => {
  const text = input.getValue()
  API.savePost({ text })
    .then(() => goTo('index.html'))
    .catch((err) => console.error(err))
})
app.append(button)

const link = new nLink()
link.setContainerStyle('text-align', 'center')
link.setContainerStyle('padding', '1rem')
link.setText('hosts')
link.href('hosts.html')
app.append(link)
