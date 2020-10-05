import * as inquirer from 'inquirer'

import Slack from './slack-api'
import Toggl from './toggl-api'

const toggl = new Toggl()
const slack = new Slack()

async function app(): Promise<void> {
  // await slack.postDailyReports()
  await Promise.all([toggl.getReports(), toggl.getTotal()]).then(
    async (res) => {
      const thoughtsText = '【思ったこと】\n\n'
      const tasksText = '\n【次やること】\n[ ] \n[ ] \n\n'
      const reportsText = `### Activity Timeline\n${res[0]}\n### Total\n${res[1]}`
      await inquirer
        .prompt({
          name: '日報を投稿する',
          type: 'editor',
          default: thoughtsText + tasksText + reportsText
        })
        .then((ans) => {
          console.log(ans)
        })
        .catch((err) => {
          console.log(err)
        })
    }
  )
}
app()
