from agithub.GitHub import GitHub # Access GitHub


class GitHubManager():

    # Load all user repositories, search for PROJECT_NAME and get release url
    def getRepositories():
        # Authorize user
        print('Load repositories')
        g = GitHub(token=IOS_GITHUB_TOKEN)
        repos = g.repos['involvestecnologia']['agilepromoter-ios'].releases.get()
        for r in repos[1]:
            tag = r['tag_name']
            if tag.decode('utf-8') == VERSION.decode('utf-8'):
                assetid = repos[1][0]['assets'][0]['id']
                url = "https://api.github.com/repos/involvestecnologia/agilepromoter-ios/releases/assets/***?access_token=c5f34972b9eae809060d3bc22dffbd006357a3b1"		
                url = url.replace('***', str(assetid))
                return url