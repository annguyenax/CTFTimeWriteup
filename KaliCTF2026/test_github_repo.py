import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.github.com/users/nullvoyager1/repos"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    repos = json.loads(response.read().decode('utf-8'))
    for repo in repos:
        repo_name = repo['name']
        print(f"Repo: {repo_name}")
        commits_url = f"https://api.github.com/repos/nullvoyager1/{repo_name}/commits"
        req_commits = urllib.request.Request(commits_url, headers={'User-Agent': 'Mozilla/5.0'})
        res_commits = urllib.request.urlopen(req_commits, context=ctx)
        commits = json.loads(res_commits.read().decode('utf-8'))
        for commit in commits:
            print("Commit message:", commit['commit']['message'])
except Exception as e:
    print(e)
