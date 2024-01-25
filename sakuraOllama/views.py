from django.http import HttpResponse, HttpResponseRedirect, httpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader

from django.shortcuts import render
from django.views import generic
# Create your views here.

def sakura(request):
  title = 'Sakura'
  chatStream = ""
  sakuraHtml = loader.get_template('sakuraOllama/sakura.html')

  if request.method == 'POST':
    # Do something
    chatStream = request.POST['chatStream']
    return HttpResponse(chatStream)
  return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'chatStream': chatStream})