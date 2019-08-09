let fetcher = require('github-graphql-fetcher/lib/client')
let csv = require('csv')
let fs = require('fs')


let csv_file = fs.readFileSync(process.argv[2])
let projects = csv.

token = process.argv[3]

client = new fetcher.GitHubClient({ tokens: [token] })
console.log(client)
console.log(csv_file)