// import ollama from 'ollama'

// const response = await ollama.chat({
//   model: 'mistral',
//   messages: [{ role: 'user', content: 'Pourquoi le ciel est bleu ?' }],
// })
// console.log(response.message.content)

const chatStreamContainer = document.querySelector('#chatStreamContainer');

windows.scrollTo(0, chatStreamContainer.scrollHeight, behavior = 'smooth', block = 'end', inline = 'nearest');