import os
import sys
import requests
import argparse
import datetime
from requests.auth import HTTPBasicAuth
from slack import WebClient
from dotenv import load_dotenv
load_dotenv()

def main():
    togglApi = TogglAPI()
    slackApi = SlackAPI()
    argparser = argparse.ArgumentParser(description='daily-report-cli')
    argparser.add_argument('-m', '--message', type=str,nargs='+', action='append', help='')
    args = argparser.parse_args()
    message = '\n'.join(sum(args.message, []))
    today = datetime.date.today()
    togglApi.get_reports(today)
    # slackApi.post_slack(message)


class TogglAPI:
    def __init__(self):
        self.api_token = os.environ.get('toggl_api_token')
        self.mail_address = os.environ.get('toggl_mail_address')
        self.workspace_id = os.environ.get('toggl_workspace_id')

    def get_reports(self, date):
        params = {
            'user_agent': self.mail_address,
            'workspace_id': self.workspace_id,
            'since': date,
            'until': date,
            'order_desc': 'off'
        }
        r = requests.get('https://toggl.com/reports/api/v2/details',
                        auth=HTTPBasicAuth(self.api_token, 'api_token'),
                        params=params)
        json_r = r.json()
        def get_activities(n):
            startDate, endDate = datetime.datetime.fromisoformat(n['start']), datetime.datetime.fromisoformat(n['end'])
            return {
                'id': n['id'],
                'start': "{}:{}:{}".format(startDate.hour, startDate.minute, startDate.second),
                'end': "{}:{}:{}".format(endDate.hour, endDate.minute, endDate.second),
                'description': n['description']
            }
        activities = list(map(get_activities, json_r['data']))
        for activity in activities:
            act = "{} - {} | {}".format(activity['start'], activity['end'], activity['description'])
            print(act)


class SlackAPI:
    def __init__(self):
        self.token = os.environ.get('slack_token')
        self.channel = os.environ.get('slack_channel')
    def post_slack(self, message):
        client = WebClient(self.token)
        content = sys.argv[1]
        response = client.files_upload(
            channels=self.channel,
            title='【日報】',
            content=message,
            filetype='post')
        assert response["file"]
