import os
import time
import json
from slack_web_client import SlackWebClient

class SlackMessage:
  def __init__(self, text, reactions):
    self._text = text
    self._reactions = reactions
    
  def getText(self):
    return self._text

  def hasReaction(self, hasReaction):
    return bool([reaction for reaction in self._reactions if hasReaction in reaction])

  def __str__(self):
    return self._text + "[" + ",".join(self._reactions) + "]"

class SlackChannelReader:
  def __init__(self, slackWebClient, channel = None):
    self._slack = slackWebClient
    self._channel = channel
  
  def scan(self, messageClosure):
    conversation_cursor = ""
    conversation = None
    while True:
      conversation = self._slack.conversations_history(
        channel = self._channel,
        cursor = conversation_cursor,
        limit = 1000
      )
      conversation_cursor = conversation["response_metadata"]["next_cursor"]
      
      for message in conversation['messages']:
        if "thread_ts" not in message:
          continue
  
        message_ts = message['ts']
        thread_ts = message['thread_ts']    
        replies = self._slack.conversations_replies(
          channel = self._channel,
          ts = message_ts,
          limit = 100
        )
      
        messageThread = []
        for reply in replies['messages']:
          reactions = []
          if 'reactions' in reply:
            for reaction in reply['reactions']:
              reactions.append(reaction['name'])
          messageThread.append(SlackMessage(reply['text'], reactions))

        messageClosure(messageThread)  

       

  
