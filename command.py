from togglClass import TogglAPI
from slackClass import SlackAPI
import datetime

togglApi = TogglAPI()
slackApi = SlackAPI()

def main(args):
    today = datetime.date.today()
    did = ''
    message = '\n'.join(sum(args.message, []))
    next = '\n'.join(sum(args.next, []))
    if args.did:
        if args.did[0][0] == 'toggl':
            activity = togglApi.get_details(today)
            total = togglApi.get_summary(today)
            did = '\nActivity:\n{}\n\nTotal:\n{}'.format(activity, total)
        else:
            did = '\n'.join(sum(args.did, []))
    content = '【やったこと】\n{}\n\n\n【思ったこと】\n{}\n\n\n【次回やること】\n{}'.format(did, message, next)
    slackApi.post_daily_report(content, today)
    if args.times:
        slackApi.post_times(next, today)

def current(args):
    current_entry = togglApi.get_current_entry()
    slackApi.update_status(current_entry)