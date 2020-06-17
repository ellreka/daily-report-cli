import os
import requests
import json
from slack import WebClient
from dotenv import load_dotenv
load_dotenv()

class SlackAPI:
    def __init__(self):
        self.token = os.environ.get('slack_token')
        self.channel = os.environ.get('slack_channel')
        self.times_channel = os.environ.get('slack_times_channel')

    def post_daily_report(self, content, today):
        client = WebClient(self.token)
        response = client.files_upload(
            channels=self.channel,
            title="【日報】{}".format(today),
            content=content,
            filetype='post')
        assert response["file"]

    def post_times(self, text, today):
        client = WebClient(self.token)
        response = client.chat_postMessage(
            channel=self.times_channel,
            text="```{}```".format(text))
        assert response

    def update_status(self, current):
        if  current is not None:
            params = {
                "token": self.token,
                "profile": json.dumps({
                    "status_text": current['description'],
                    "status_emoji": ':dart:'
                })
            }
            requests.post('https://slack.com/api/users.profile.set', params=params)