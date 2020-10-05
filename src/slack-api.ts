import fetch, { Headers } from 'node-fetch'

import { config } from './config'

export default class Slack {
  slack_token = config().toggl_api_token
  slack_channel = config().slack_channel
  slack_times_channel = config().slack_times_channel

  async postDailyReports(): Promise<void> {
    const headers = new Headers({
      Authorization:
        'Bearer " ' + Buffer.from(`${this.slack_token}`).toString('base64')
    })

    const today = new Date().toISOString()

    const params = {
      channels: this.slack_channel,
      title: `【日報】${today}`,
      content: 'aaaaa',
      filetype: 'post'
    }
    try {
      const response = await fetch('https://slack.com/api/files.upload', {
        method: 'POST',
        headers,
        body: JSON.stringify(params)
      })
      console.log(response)
    } catch (err) {
      console.log(err)
    }
  }
}
