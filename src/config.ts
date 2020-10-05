import { ConfigType } from './types'

const defaultEnv = {
  toggl_api_token: '',
  toggl_workspace_id: '',
  toggl_mail_address: '',
  slack_token: '',
  slack_channel: '',
  slack_times_channel: ''
}

export const config = (): ConfigType => {
  try {
    return require('../.env.json')
  } catch {
    return defaultEnv
  }
}
