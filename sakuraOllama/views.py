from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from django.shortcuts import render
from django.views import generic
# Create your views here.

def sakura(request):
  title = 'Sakura Ollama'
  return render(request, 'sakuraOllama/sakura.html', {'page_title': title})