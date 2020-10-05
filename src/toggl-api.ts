import { format } from 'date-fns'
import fetch, { Headers } from 'node-fetch'
import { URL, URLSearchParams } from 'url'

import { config } from './config'
import { TogglDetails, TogglSummaries } from './types'

export default class Toggl {
  mail_address = config().toggl_mail_address
  workspace_id = config().toggl_workspace_id
  api_token = config().toggl_api_token

  async getDetails(): Promise<TogglDetails> {
    const headers = new Headers({
      Authorization:
        'Basic ' + Buffer.from(`${this.api_token}:api_token`).toString('base64')
    })

    const today = new Date().toISOString()

    const params = new URLSearchParams({
      user_agent: this.mail_address,
      workspace_id: this.workspace_id,
      since: today,
      until: today,
      order_desc: 'off'
    }).toString()
    try {
      const response = await fetch(
        new URL(`https://toggl.com/reports/api/v2/details?${params}`),
        {
          method: 'GET',
          headers
        }
      )
      const r = await response.json()
      return r.data.map((detail: any) => {
        return {
          id: detail.id,
          project: detail.project,
          description: detail.description,
          start: new Date(detail.start),
          end: new Date(detail.end),
          dur: detail.dur
        }
      })
    } catch (err) {
      return err
    }
  }

  async getSummaries(): Promise<TogglSummaries> {
    const headers = new Headers({
      Authorization:
        'Basic ' + Buffer.from(`${this.api_token}:api_token`).toString('base64')
    })

    const today = new Date().toISOString()

    const params = new URLSearchParams({
      user_agent: this.mail_address,
      workspace_id: this.workspace_id,
      since: today,
      until: today
    }).toString()
    try {
      const response = await fetch(
        new URL(`https://toggl.com/reports/api/v2/summary?${params}`),
        {
          method: 'GET',
          headers
        }
      )
      const r = await response.json()
      return r.data.map((summary: any) => {
        return {
          id: summary.id,
          project: summary.title.project,
          time: summary.time,
          items: summary.items.map((item: any) => {
            return {
              title: item.title.time_entry,
              time: item.time
            }
          })
        }
      })
    } catch (err) {
      return err
    }
  }

  async getReports(): Promise<string> {
    const details = await this.getDetails()
    let result = ''
    details.forEach((detail) => {
      const time = `${format(detail.start, 'HH:mm')} ~ ${format(
        detail.end,
        'HH:mm'
      )}`
      result += `${time} [${detail.project}] ${detail.description}\n`
    })
    return result
  }

  async getTotal(): Promise<string> {
    const summaries = await this.getSummaries()
    const formatTime = (
      dur: number
    ): {
      hours: string
      minutes: string
    } => {
      const hours = Math.floor(dur / 3600000)
      const minutes = Math.floor((dur - 3600000 * hours) / 60000)
      return {
        hours: hours.toString().padStart(2, '0'),
        minutes: minutes.toString().padStart(2, '0')
      }
    }
    let result = ''
    summaries.forEach((summary) => {
      const { hours, minutes } = formatTime(summary.time)
      let items = ''
      summary.items.forEach((item) => {
        const { hours, minutes } = formatTime(item.time)
        items += `・${item.title} (${hours}:${minutes})\n`
      })
      result += `${summary.project} (${hours}:${minutes})\n${items}\n`
    })
    return result
  }
}
