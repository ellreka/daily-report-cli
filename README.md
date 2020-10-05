# daily-report-cli

## setup

```bash
yarn
yarn dev
node build/index.js
```

### .env.json

```json
{
  "toggl_api_token": "xXxXxXxXxXxXx",
  "toggl_workspace_id": "xXxXxXxXxXxXx",
  "toggl_mail_address": "xXxXxXxXxXxXx",
  "slack_token": "xXxXxXxXxXxXx",
  "slack_channel": "xXxXxXxXxXxXx",
  "slack_times_channel": "xXxXxXxXxXxXx"
}
```

## use

### post daily report

```bash
daily-report
```

## options

```bash
  -h, --help            show this help message and exit
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
  -n NEXT [NEXT ...], --next NEXT [NEXT ...]
  -d DID [DID ...], --did DID [DID ...]
  -t, --times
```
