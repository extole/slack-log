import os
import time
import json
from slack_web_client import SlackWebClient
from slack_channel_reader import SlackChannelReader

#logChannel = "C052W445J"   # gotoperson
#logChannel = "C04SK8HBA"   # product
logChannel = "CDD4726MR"   #solutions

slack = SlackWebClient()
channelReader = SlackChannelReader(slack, 
  channel = logChannel)

def logPrompt(messageThread):
  if messageThread[0].hasReaction("ai-ignore"):
    return

  messages = []
  for message in messageThread:
    if not message.hasReaction("ai-ignore"):
      messages.append(message)      
  
  prompt = messages[0]
  for message in messageThread:
    if message.hasReaction("ai-question"):
      prompt = message
  
  if len(messages) < 1:
    return    
  replies = messages[1:]

  replies = [message for message in messages if message.hasReaction("ai-answer") or message.hasReaction("+1") ]
  
  for reply in replies:
    trainingEntry = {
     "prompt": prompt.getText(),
     "completion": reply.getText()
    }
              
    print(json.dumps(trainingEntry), file = file)
    file.flush()
    print(json.dumps(trainingEntry))
        
with open('output.jsonl', 'w') as file:
  channelReader.scan(lambda messageThread: logPrompt(messageThread))

