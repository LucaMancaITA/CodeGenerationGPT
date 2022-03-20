
import time
from datetime import datetime
from github import Github
import os
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan


end_time = time.time() # Last time
start_time = end_time - 86400

ACCESS_TOKEN = open("token.txt", "r").read()
g = Github(ACCESS_TOKEN)
print(g.get_user())


for i in range(3):
    try:
        start_time_str = datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d")
        end_time_str = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d")
        query = f"language:python created:{start_time_str}..{end_time_str}"
        print(query)
        end_time -= 86400
        start_time -= 86400

        result = g.search_repositories(query)
        print(result.totalCount)

        for repository in result:
            print(f"{repository.clone_url}")
            print(f"{repository.tags_url}")
            #print(dir(repository))

            os.system(f"git clone {repository.clone_url} repos/{repository.owner.login}/{repository.name}")

    except Exception as e:
        print(str(e))
        print(red(bold("Broke for some reason ...")))
        time.sleep(120)


print(f"Finished, your new end time should be: {start_time}")


