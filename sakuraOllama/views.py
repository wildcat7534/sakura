from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json

from django.shortcuts import render
from django.views import generic

import requests
import ollama
import markdown



def sakura(request):
  
  title = 'Répondu !'
  chatUser = "comment on dit bonjour en Japonais ?"
  if request.method == 'POST':
  
    chatUser = request.POST.get('question')
    #make a dictionnary variable to store the chat history
    chatHistory = [{'role': 'user', 'content': chatUser}, { 'role' : 'assistant', 'content': 'attente de Sakura : ' }]

    print("chatUser: ", chatUser)

    responses = []
    for chunk in ollama.chat('sakura', messages=chatHistory, stream=True):
      message = chunk['message']['content']
      print(message, end='', flush=True)
      responses.append(message)
      
    print("responses brut : ", responses)

    responsePhrases = []
    phrase = ""
    code = ""
    responseCode = ["print('Hello world !')"]

    for response in responses:
      if response != "\n":
        phrase += response
      else:
        responsePhrases.append(phrase)
        print("Phrase ajouté à responsePhrases : ", phrase)
        phrase = ""
      
    for response in responses:
      if response.startswith("``"):
        code += response
        responseCode.append(code)
        if response.startswith("`"):
          code += response
          responseCode.append(code)
          print("code ajouté à responseCode : ", code)
      
    print("chunk de phrase : ",phrase)
    print("response code : ",code)
    print("responsePhrases : ",responsePhrases)

    
  return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'userQuestion' : chatUser, 'chatStream': responsePhrases, 'codes' : responseCode})


def recupCode(reponse):
  code = ""
  for response in responses:
    code += response
    if response == "```":
      responseCodeWorking.append(code)
      print("code : ", code)
      code = ""
  return responseCodeWorking





  # completion

  # response = ollama.chat(
  #   model='sakura', 
  #   messages=[
  #     {
  #       'role': 'user',
  #       'content': chatUser,
  #     },
  #   ])
  # chatUser = response['message']['content']
  # #chatUser = markdown.markdown(chatUser)
  # #chatUser = process_gpt_output(chatUser)

  # print(chatUser)

  # chat streaming


  #return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'chatStream': chatUser})


def process_gpt_output(gpt_output):
    lines = gpt_output.split("\n")
    
    # Check if it's a numbered list
    if all(line.strip().startswith(("1.", "2.", "3.", "4.", "5.")) for line in lines if line.strip()):
        list_items = []
        for line in lines:
            line = line.strip()
            if line:
                # Extract the item after the number
                _, item = line.split(".", 1)
                list_items.append(f"<li>{item.strip()}</li>")
        if list_items:
            return "<ol>" + "\n".join(list_items) + "</ol>"

    # If the output contains multiple lines:
    elif "\n" in gpt_output:
        paragraphs = gpt_output.split("\n")
        return "".join(f"<p>{para.strip()}</p>" for para in paragraphs if para.strip())

    # Return the output as is if none of the above conditions are met
    return gpt_output