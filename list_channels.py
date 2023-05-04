import os
import time
from slack_web_client import SlackWebClient

try:
    slackBotToken = os.environ["SLACK_BOT_TOKEN"]
except KeyError:
    print("""Please setup a SLACK_BOT_TOKEN secret
- see https://api.slack.com/authentication/basics
""")
    exit(1)

slack = SlackWebClient()

cursor = ""
while True:
  response = slack.conversations_list(
    types = "public_channel",
    exclude_archived = True,
    cursor = cursor,
    limit = 5000
  )

  cursor = response["response_metadata"]["next_cursor"]

  for channel in response['channels']:
    print(channel['name'])

  if len(response['channels']) == 0:
    break