export type TogglDetails = Array<{
  id: number
  project: string
  description: string
  start: Date
  end: Date
  dur: number
}>

export type TogglSummaries = Array<{
  id: number
  project: string
  time: number
  items: Array<{
    title: string
    time: number
  }>
}>

export interface ConfigType {
  toggl_api_token: string
  toggl_workspace_id: string
  toggl_mail_address: string
  slack_token: string
  slack_channel: string
  slack_times_channel: string
}
