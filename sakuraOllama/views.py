from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json

from django.shortcuts import render
from django.views import generic

import requests
import ollama

def sakura(request):

  title = 'Sakura'
  chatBody = "attente"

  if request.method == 'POST':
       
    chatBody = request.POST.get('question')
        
    print("chatBody: ", chatBody)

    data = {'model': 'sakura', 'prompt': 'why the sky is blue'}
    #post the server ollama with the data and with the -d option in the paramaters ?

    ollama_response = requests.post('http://localhost:11434/api/generate', data=data )
    print(ollama_response)

    # response = ollama.chat(model='sakura', messages=[
    #  {
    #   'role': 'user',
    #   'content': chatBody,
    # },
    # ])
    # chatBody = response['message']['content']

    #print(ollama_response)


  return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'chatStream': chatBody})



    # message = json.loads(chatBody)['message']
    # chatStream = request.POST['chatStream']
    # chatStream2 = request.parse_body()
