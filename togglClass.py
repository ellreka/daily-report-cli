import os
import requests
import json
import datetime
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

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
        total_text = ""
        for t in total:
            item_text = ""
            for i in t['items']:
                item_text += "{} ({})\n".format(i['title'], datetime.timedelta(milliseconds=i['time']))
            total_text += "{} ({})\n{}\n\n".format(
                t['project_name'], datetime.timedelta(milliseconds=t['time']), item_text)
        return total_text

    def get_current_entry(self):
        r = requests.get('https://www.toggl.com/api/v8/time_entries/current',
            auth=HTTPBasicAuth(self.api_token, 'api_token'))
        json_r = r.json()
        return json_r['data']