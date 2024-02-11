from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import loader
import json

from django.views import generic

""" import requests
import asyncio
import markdown
import ollama
#for vLLM
from vllm import LLM, SamplingParams """

from asgiref.sync import async_to_sync
from httpx import Client
from ollama._client import BaseClient
#for Transformers
""" from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch """

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from ollama import AsyncClient
import asyncio

title = 'Répondu !'
conversation = []
phrasesSakura = []
phrasesUser = []
chatUser = ""

def sakuraAsync(request):
  global conversation, phrasesSakura, phrasesUser, chatUser
 
  async def main():
    phraseUser = ''.join(chatUser)
    phrasesUser.append(phraseUser)
    print("phraseUser : ", phraseUser)
    phrasesSakura.append(await chat(conversation))
    print("phrasesSakura : ", phrasesSakura)
  
  if request.method == 'POST':
    if request.POST.get('question') != '':
      chatUser = request.POST.get('question')
    else:
      chatUser = "je ne sais pas quoi dire..."

    # // AsyncClient().
    async def chat(conversation):
      client = AsyncClient(host='http://192.168.0.100:11434')
      generated_text_buff = []
      async for part in await client.chat(model='sakura', messages=conversation, stream=True):

        generated_text_buff += (part['message']['content'])
        phrase = ''.join(generated_text_buff)
      
      conversation.append({'role': 'assistant', 'content': phrase})
      return phrase
    
    chatUser = request.POST.get('question')
    conversation.append({'role': 'user', 'content': chatUser})
    asyncio.run(main())
    return render(request, 'sakuraOllama/sakuraasync.html', {'page_title': title, 'userAnswer' : phrasesUser, 'chatStream': phrasesSakura, 'conversation' : conversation })
    

  return render(request, 'sakuraOllama/sakuraasync.html', {'page_title': title, 'userQuestion' : "Sakura attend", 'chatStream': ""})
    #phrasesSakura.append( async_to_sync(chat)(conversation) )
    #print("taille de conversation : ", len(conversation), "selectionne le dernier element : ", conversation[len(conversation)-2]['content'] , conversation[len(conversation)-1]['content'])






""" def sakuraVllm(request):
  chatUser = "Comment on dit bonjour en Japonais ?"
  generated_text = ""
  if request.method == 'POST':

    chatUser = request.POST.get('question')

    prompts = [
      chatUser,
    ]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
    #llm = LLM(model="sakura")
    llm = LLM(model="mistralai/Mistral-7B-v0.1", max_model_len=1024, gpu_memory_utilisation=0.9, device_map = "auto")
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
  outputs = pipeline(prompt, streamer=streamer, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95) """


