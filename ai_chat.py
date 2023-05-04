import os
import openai
import logging
import datetime
import time

try:
  openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
  print("""Please setup an OPENAI_API_KEY secret.
  - get an openapi secret here:  
    https://platform.openai.com/account/api-keys
  - see here on how to setup a secret: 
    https://docs.replit.com/programming-ide/workspace-features/storing-sensitive-information-environment-variables
""" )
  exit(1)

defaultModel = "gpt-3.5-turbo"

class Ai:
  def __init__(self):
    global defaultModel
    self._model = defaultModel
    self._logger = logging.NullHandler
    
  def listModels(self):
    response = []
    try:
      response = openai.Model.list()
    except Exception as e:
      return [ "no-response" ]
    
    models = []
    for model in response["data"]:
      models.append(model["id"])
      
    return models

  def getModel(self):
    return self._model

  def withModel(self, model):
    models = self.listModels()

    if model in models:
      print("set model", model)
      self._model = model
    
  def createChat(self, name):
    return AiChat(name)


class AiChat:
  def __init__(self, name):
    global defaultModel
    
    self._name = name
    self._messages = []
    self._model = defaultModel
    self._logger = logging.NullHandler

  def withModel(self, model):
    self._model = model

  def withLogger(self, logger):
    self._logger = logger
    
  def talk(self, content):
    self.addUserMessage(content)
    return self.send()
    
  def addInitialSystemMessage(self, content):
    self.addMessage("system", content, "forever")
  
  def addSystemMessage(self, content):
    self.addMessage("system", content)

  def addAssistantMessage(self, content):
    self.addMessage("assistant", content)

  def addUserMessage(self, content):
    self.addMessage("user", content)

  def addMessage(self, role, content, keep = "asLongAsPossible"):

    self._messages.append({
      "role": role,
      "content": content,
      "keep": keep
    })

  def send(self):
    response = None
    retryCount = 0
    while retryCount < 5:
      messages = []      
      for message in self._messages:
        messages.append({
          "role": message['role'],
          "content": message['content']
        })
        
      try:
        response = openai.ChatCompletion.create(
          model = self._model, 
          messages = messages,
          max_tokens = 200,
          temperature = 0.9)
      except openai.error.InvalidRequestError as e:
        for index, message in enumerate(self._messages):
          if message["keep"] == "asLongAsPossible":
            self._messages.pop(index)
            break
      except Exception as e:
        retryCount += 1
      else:
        break

    if response is None:
      return { "role": "assistant", "content": "No Response" }
      
    message = response.choices[0].message.content
    
    self._messages.append({
      "role": "assistant", 
      "content": message,
      "keep": "asLongAsPossible",
    })

    return message
