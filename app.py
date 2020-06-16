import os
import sys
import requests
import json
import argparse
import datetime
from requests.auth import HTTPBasicAuth
from slack import WebClient
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
load_dotenv()


def main():
    togglApi = TogglAPI()
    slackApi = SlackAPI()
    argparser = argparse.ArgumentParser(description='daily-report-cli')
    subparsers = argparser.add_subparsers(dest='subparser_name')
    subparsers.required = False
    current_parser = subparsers.add_parser('current', help='')
    current_parser.set_defaults(func=current)
    argparser.add_argument('-m', '--message', type=str, 
    nargs='+', action='append', default=[], required=False, help='')
    argparser.add_argument('-n', '--next', type=str,
    nargs='+', action='append', default=[], required=False, help='')
    argparser.add_argument('-d', '--did', type=str,
    default=[], required=False, help='')
    argparser.add_argument('-t', '--times', default=False,
    type=bool, required=False, help='')
    args = argparser.parse_args()
    if hasattr(args, 'func'):
        args.func()
    else:
        print('サブコマンドを指定して下さい')
    # message = '\n'.join(sum(args.message, []))
    # next = '\n'.join(sum(args.next, []))
    # today = datetime.date.today()

    # if args.did == 'toggl':
    #     activity = togglApi.get_details(today)
    #     total = togglApi.get_summary(today)
    #     did = "\nActivity:\n{}\n\nTotal:\n{}".format(activity, total)
    # else:
    #     did = args.did

    # content = "【やったこと】\n{}\n\n\n【思ったこと】\n{}\n\n\n【次回やること】\n{}".format(
    #     did, message, next)
    # slackApi.post_daily_report(content, today)
    # if args.times:
    #     slackApi.post_times(next, today)
    # togglApi.get_summary(today)
    # if current:
    #     print('current')
    #     current_entry = togglApi.get_current_entry()
    #     slackApi.update_status(current_entry)

def current():
    print('current!!')
    togglApi = TogglAPI()
    slackApi = SlackAPI()
    current_entry = togglApi.get_current_entry()
    slackApi.update_status(current_entry)


class TogglAPI:
    def __init__(self):
        self.api_token = os.environ.get('toggl_api_token')
        self.mail_address = os.environ.get('toggl_mail_address')
        self.workspace_id = os.environ.get('toggl_workspace_id')

    def get_details(self, date):
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
            startDate, endDate = datetime.datetime.fromisoformat(
                n['start']), datetime.datetime.fromisoformat(n['end'])
            return {
                'id': n['id'],
                'start': "{}:{}:{}".format(startDate.hour, str(startDate.minute).zfill(2), str(startDate.second).zfill(2)),
                'end': "{}:{}:{}".format(endDate.hour, endDate.minute, endDate.second),
                'description': n['description']
            }
        activities = list(map(get_activities, json_r['data']))
        activitiy_text = ""
        for activity in activities:
            activitiy_text += "{} : {} \n".format(
                activity['start'], activity['description'])
        return activitiy_text

    def get_summary(self, date):
        params = {
            'user_agent': self.mail_address,
            'workspace_id': self.workspace_id,
            'since': date,
            'until': date,
        }
        r = requests.get('https://toggl.com/reports/api/v2/summary',
        auth=HTTPBasicAuth(self.api_token, 'api_token'),
        params=params)
        json_r = r.json()

        def get_total(n):
            return {
                'id': n['id'],
                'color': n['title']['hex_color'],
                'project_name': n['title']['project'],
                'time': n['time'],
                'items': list(map(lambda y: {'title': y['title']['time_entry'], 'time': y['time']}, n['items']))
            }
        total = list(map(get_total, json_r['data']))
        create_graph(total)
        total_text = ""
        for t in total:
            item_text = ""
            for i in t['items']:
                item_text += "・{} ({})\n".format(i['title'],
                datetime.timedelta(milliseconds=i['time']))
            total_text += "{} ({})\n{}\n\n".format(
                t['project_name'], datetime.timedelta(milliseconds=t['time']), item_text)
        return total_text

    def get_current_entry(self):
        r = requests.get('https://www.toggl.com/api/v8/time_entries/current',
            auth=HTTPBasicAuth(self.api_token, 'api_token'))
        json_r = r.json()
        return json_r['data']


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
        print(self.times_channel)
        print(text)
        client = WebClient(self.token)
        response = client.chat_postMessage(
            channel=self.times_channel,
            text="```{}```".format(text))
        assert response

    def update_status(self, current):
        description = current['description'] if current is not None else ''
        params = {
            "token": self.token,
            "profile": json.dumps({
                "status_text": description,
                "status_emoji": ''
            })
        }
        requests.post(
            'https://slack.com/api/users.profile.set', params=params)


def create_graph(data):
    label = list(map(lambda n: n['project_name'], data))
    colors = list(map(lambda n: n['color'], data))
    x = np.array(list(map(lambda n: n['time'], data)))
    plt.pie(x, labels=label, colors=colors, counterclock=False, startangle=90)
    plt.savefig('figure.png')
