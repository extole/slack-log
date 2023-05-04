
import os
import time
import socket
import requests
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry import (RetryHandler, RetryState, HttpRequest, HttpResponse)
from slack_sdk.http_retry.builtin_interval_calculators import BackoffRetryIntervalCalculator
from slack_sdk.http_retry.jitter import RandomJitter



try:
    slackBotToken = os.environ["SLACK_BOT_TOKEN"]
except KeyError:
    print("""Please setup a SLACK_BOT_TOKEN secret
- see https://api.slack.com/authentication/basics
""")
    exit(1)


class SlackRetryHandler(RetryHandler):
    def _can_retry(
        self,
        *,
        state: RetryState,
        request: HttpRequest,
        response: Optional[HttpResponse] = None,
        error: Optional[Exception] = None
    ) -> bool:
        #print("ERROR", error, state, response)
        if error is None:
          #print("NO ERROR RETRY")
          return True
        if error.code == 104:
          #print("HTTP CODE 104")
          return True
        if error.code == 429:
          #print("HTTP CODE 429")
          delay = 1
          if response is not None:
            delay = int(response.headers['Retry-After'][0])
          time.sleep(delay)
          #print("DELAYED RETRY")
          return True
        else:
          #print("NO RETRY")
          return False

class SlackWebClient(WebClient):
    def __init__(self):
      super().__init__(
        token = slackBotToken,
        retry_handlers = [
          SlackRetryHandler(
            max_retry_count = 2,
            interval_calculator = BackoffRetryIntervalCalculator(
              backoff_factor = 0.5,
              jitter = RandomJitter()
            )
          )],
      )

