from togglClass import TogglAPI
from slackClass import SlackAPI

a = 'aaaa'
togglApi = TogglAPI()
slackApi = SlackAPI()

def main(args):
    message = '\n'.join(sum(args.message, []))
    next = '\n'.join(sum(args.next, []))
    today = datetime.date.today()

    if args.did == 'toggl':
        activity = togglApi.get_details(today)
        total = togglApi.get_summary(today)
        did = "\nActivity:\n{}\n\nTotal:\n{}".format(activity, total)
    else:
        did = args.did

    content = "【やったこと】\n{}\n\n\n【思ったこと】\n{}\n\n\n【次回やること】\n{}".format(
        did, message, next)
    print(did, message, next)
    # slackApi.post_daily_report(content, today)
    if args.times:
        print('post #times')
        # slackApi.post_times(next, today)

def current(args):
    print(args)
    print('current!!')
    current_entry = togglApi.get_current_entry()
    slackApi.update_status(current_entry)