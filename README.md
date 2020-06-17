# daily-report-cli

## setup
```bash
pip3 install -e .
```

### .env
```
toggl_api_token=xXxXxXxXxXxXx
toggl_workspace_id=xXxXxXxXxXxXx
toggl_mail_address=xXxXxXxXxXxXx
slack_token=xoxp-xXxXxXxXxXxXx
slack_channel=xXxXxXxXxXxXx
slack_times_channel=xXxXxXxXxXxXx
```

## use
### post daily report
```bash
daily-report -m "foo" -m "bar"
```

### update slack status
```bash
daily-report current
```

## options
```bash
  -h, --help            show this help message and exit
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
  -n NEXT [NEXT ...], --next NEXT [NEXT ...]
  -d DID [DID ...], --did DID [DID ...]
  -t, --times
```
