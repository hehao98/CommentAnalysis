/*
 * Fetch project information from GitHub
 * Usage: node FetchProjectInfo.js [CSV Path] [GitHub Access Token]
 */

let fetcher = require('github-graphql-fetcher/lib/client')
let csv = require('csvtojson')
let fs = require('fs')

let csvPath = process.argv[2]
let token = process.argv[3]

if (!fs.existsSync('result/ProjectInfo/')) {
    fs.mkdirSync('result/ProjectInfo/')
}

csv().fromFile(csvPath).then(async function (projects) {
    let client = new fetcher.GitHubClient({ tokens: [token] })
    await client.init()
    promises = []
    for (let i = 0; i < projects.length; ++i) {
        let proj = projects[i]

        if (fs.existsSync('result/ProjectInfo/' + proj['name'] + '.json')) {
            console.log('Skipping project ' + i + ': ' + proj['name'])
            continue
        }

        let owner = proj['name'].split('_')[0]
        let name = proj['name'].split('_')[1]

        proj['info'] = await client.repo.info(owner, name)
        proj['pull_requests'] = await client.repo.pulls(owner, name)
        proj['issues'] = await client.repo.issues(owner, name)
        proj['contributors'] = await client.repo.contributors(owner, name, 'master')  
        fs.writeFileSync('result/ProjectInfo/' + proj['name'] + '.json', JSON.stringify(proj, null, 2))
        console.log('Project ' + i + ' Finished')
    }
})



