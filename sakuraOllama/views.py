from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json

from django.shortcuts import render
from django.views import generic

import requests
import ollama
import markdown
#for vLLM
from vllm import LLM, SamplingParams
#for Transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

title = 'Répondu !'


def sakura(request):
  
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


def sakuraVllm(request):
  chatUser = "Comment on dit bonjour en Japonais ?"
  generated_text = ""
  if request.method == 'POST':

    chatUser = request.POST.get('question')

    prompts = [
      chatUser,
    ]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
    #llm = LLM(model="sakura")
    #llm = LLM(model="mistralai/Mistral-7B-v0.1")
    llm = AutoModelForCausalLM.from_pretrained("")

    outputs = llm.generate(prompts, sampling_params)

    # print the outputs
    for output in outputs:
      prompt = output.prompt
      generated_text = output.output[0].text
      affiche = generated_text.join(prompt)
      print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    
    return render(request, 'sakuraOllama/sakuravllm.html', {'page_title': title, 'userQuestion' : chatUser, 'chatStream': affiche})
  return render(request, 'sakuraOllama/sakuravllm.html', {'page_title': title, 'userQuestion' : chatUser, 'chatStream': generated_text})

def sakuraTransormers(request):
  chatUser = "Comment on dit bonjour en Japonais ?"
  generated_text = ""
  if request.method == 'POST':

    chatUser = request.POST.get('question')

    from transformers import AutoTokenizer


  model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
  tokenizer = AutoTokenizer.from_pretrained(model)

  pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    model_kwargs={"torch_dtype": torch.float16, "load_in_4bit": True},
  )

  messages = [{"role": "user", "content": "Explain what a Mixture of Experts is in less than 100 words."}]
  prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

  from transformers import TextStreamer
  streamer = TextStreamer(tokenizer, skip_prompt=True)
  outputs = pipeline(prompt, streamer=streamer, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
