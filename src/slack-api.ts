import { WebClient } from '@slack/web-api'

import { config } from './config'

export default class Slack {
  slack_token = config().slack_token
  slack_channel = config().slack_channel
  slack_times_channel = config().slack_times_channel

  async postDailyReports(content: string): Promise<void> {
    const web = new WebClient(this.slack_token)
    const today = new Date().toISOString()
    const params: { [key: string]: string } = {
      channels: this.slack_channel,
      title: `【日報】${today}`,
      content,
      filetype: 'post'
    }
    try {
      await web.files.upload(params)
    } catch (err) {
      console.log(err)
    }
  }
}
