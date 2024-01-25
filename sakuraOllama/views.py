from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json

from django.shortcuts import render
from django.views import generic
# Create your views here.

def sakura(request):
  title = 'Sakura'
  chatBody = "attente"

  if request.method == 'POST':
    # Do something
    print("POST request", request.POST)
       
    chatBody = request.POST.get('text')
        
    print("chatBody: ", chatBody)
    return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'chatStream': chatBody})
    # message = json.loads(chatBody)['message']
    # chatStream = request.POST['chatStream']
    # chatStream2 = request.parse_body()
