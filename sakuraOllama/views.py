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

    response = ollama.chat(
      model='sakura', 
      messages=[
        {
          'role': 'user',
          'content': chatBody,
        },
      ])
    chatBody = response['message']['content']

    print(chatBody)

  return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'chatStream': chatBody})


