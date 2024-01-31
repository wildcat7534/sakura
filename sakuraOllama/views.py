from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
import json

from django.shortcuts import render
from django.views import generic

import requests
import asyncio
import ollama
from ollama import AsyncClient
from asgiref.sync import async_to_sync
import markdown
#for vLLM
from vllm import LLM, SamplingParams
#for Transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

title = 'Répondu !'


def sakura(request):
  responsePhrases = []
  chatUser = "Comment on dit bonjour en Japonais ?"

  if request.method == 'POST':
  
    chatUser = request.POST.get('question')

    chatHistory = [{'role': 'user', 'content': chatUser}]

    print("chatUser: ", chatUser)

    responses = []
    for chunk in ollama.chat('sakura', messages=chatHistory, stream=True):
      message = chunk['message']['content']
      print( message, end='', flush=True)
      responses.append(message)
      
    print("responses brut : ", responses)

    responsePhrases = []
    phrase = ""

    for response in responses:
      if response != "\n":
        phrase += response
      else:
        responsePhrases.append(phrase)
        print("Phrase ajouté à responsePhrases : ", phrase)
        phrase = ""
      
    print("chunk de phrase : ",phrase)
    print("responsePhrases : ",responsePhrases)

    
    return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'userQuestion' : chatUser, 'chatStream': responsePhrases} )
  return render(request, 'sakuraOllama/sakura.html', {'page_title': title, 'userQuestion' : chatUser, 'chatStream': responsePhrases} )

phrases = []
conversation = [{'role': 'user', 'content': 'start' }, {'role': 'assistant', 'content': 'start'}]

def sakuraAsync(request):
 
  if request.method == 'POST':

    global conversation, phrases

    async def chat(conversation):
      generated_text_buff = []

      #messages = [message['content'] for message in conversation if isinstance(message['content'], str) and message['content']]

      async for part in await AsyncClient().chat(model='sakura', messages=conversation, stream=True):

        generated_text_buff += (part['message']['content'])
        phrase = ''.join(generated_text_buff)
      
      conversation.append({'role': 'assistant', 'content': phrase})

      return phrase
    
    chatUser = request.POST.get('question')
    conversation.append({'role': 'user', 'content': chatUser})

    phrase = async_to_sync(chat)(conversation)

    phrases.append(phrase)

    return render(request, 'sakuraOllama/sakuraasync.html', {'page_title': title, 'userAnswer' : conversation[0]['content'], 'chatStream': phrases})
  return render(request, 'sakuraOllama/sakuraasync.html', {'page_title': title, 'userQuestion' : "Sakura attend", 'chatStream': ""})

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
    llm = LLM(model="mistralai/Mistral-7B-v0.1", max_model_len=1024, gpu_memory_utilisation=0.9)
    #llm = AutoModelForCausalLM.from_pretrained("")

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


  model = "mistralai/Mistral-7B-v0.1"

  tokenizer = AutoTokenizer.from_pretrained(model)

  pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    model_kwargs={"torch_dtype": torch.float16, "load_in_4bit": True, "gpu_memory_utilisation": 0.9}
  )

  messages = [{"role": "user", "content": "Explain what a Mixture of Experts is in less than 100 words."}]
  prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

  from transformers import TextStreamer
  streamer = TextStreamer(tokenizer, skip_prompt=True)
  outputs = pipeline(prompt, streamer=streamer, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)


